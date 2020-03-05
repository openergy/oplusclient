from getpass import getpass
import os
import datetime as dt
import json
import base64

import requests
from requests.auth import AuthBase

from .task import Task
from .exceptions import InvalidToken


class RestClient:
    def __init__(
            self,
            api_token=None,
            base_url="https://oplus-back.openergy.fr/api/v1"
    ):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self._session = requests.Session()
        self._session.auth = _JWTAuth(
            api_token if api_token is not None else getpass("Api token: "),
            self.base_url
        )

    def list(self, path, params=None):
        response = self._session.get(
            f"{self.base_url}/{path}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def create(self, path, data):
        response = self._session.post(
            f"{self.base_url}/{path}",
            json=data
        )
        response.raise_for_status()
        return response.json()

    def retrieve(self, path, record_id, params=None):
        response = self._session.get(
            f"{self.base_url}/{path}/{record_id}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def update(self, path, record_id, data):
        response = self._session.put(
            f"{self.base_url}/{path}/{record_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()

    def delete(self, path, resource_id):
        response = self._session.delete(
            f"{self.base_url}/{path}/{resource_id}"
        )
        response.raise_for_status()

    def detail_action(self, path, record_id, action_name, method="get", data=None, params=None):
        response = self._session.request(
            method,
            f"{self.base_url}/{path}/{record_id}/{action_name}",
            json=data,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def download(self, download_url, buffer_or_path=None):
        response = self._session.get(
            download_url
        )
        response.raise_for_status()
        if isinstance(response.content, bytes):
            if buffer_or_path is None:
                return response.content
            else:
                if hasattr(buffer_or_path, "write"):
                    buffer_or_path.write(response.content)
                else:
                    with open(buffer_or_path, "wb") as f:
                        f.write(response.content)
        elif isinstance(response.content, str):
            if buffer_or_path is None:
                return response.content.encode("utf-8")
            else:
                if hasattr(buffer_or_path, "write"):
                    buffer_or_path.write(response.content)
                else:
                    with open(buffer_or_path, "w") as f:
                        f.write(response.content)
        else:
            raise ValueError("Response content is neither str nor bytes")

    def upload(self, upload_url, buffer_or_path):
        if hasattr(buffer_or_path, "read"):
            response = self._session.put(
                upload_url,
                buffer_or_path.read(),
                headers={"x-ms-blob-type": "BlockBlob"}
            )
        else:
            with open(os.path.realpath(buffer_or_path), "rb") as f:
                response = self._session.put(
                    upload_url,
                    f.read(),
                    headers={"x-ms-blob-type": "BlockBlob"}
                )
        response.raise_for_status()


class _JWTAuth(AuthBase):
    def __init__(self, refresh_token, base_url):
        self._token_url = f"{base_url.strip('/')}/oteams/token/refresh"
        self._refresh_token = refresh_token
        self._refresh_token_exp = self._get_token_exp(refresh_token)
        self._access_token, self._access_token_exp = self._get_access_token()

    def __call__(self, r):
        if self._access_token_exp - dt.datetime.utcnow() < dt.timedelta(seconds=1):
            self._access_token, self._access_token_exp = self._get_access_token()
        r.headers["Authorization"] = f"Bearer {self._access_token}"
        return r

    def _get_access_token(self):
        # check if token expired
        if self._refresh_token_exp - dt.datetime.utcnow() < dt.timedelta(seconds=1):
            raise InvalidToken("Api token expired.")
        r = requests.post(self._token_url, json=dict(refresh=self._refresh_token))
        if r.status_code == 401:
            raise InvalidToken("Api token was refused by the server.")
        r.raise_for_status()
        token = r.json()["access"]
        return token, self._get_token_exp(token)

    @staticmethod
    def _decode_token(token):
        if isinstance(token, str):
            token = token.encode("utf-8")
        try:
            payload = token.rsplit(b".", 1)[0].split(b".", 1)[1]
            payload += b"=" * max(0, (4 - (len(payload) % 4)))  # padding
            payload = base64.urlsafe_b64decode(payload)
            data = json.loads(payload.decode("utf-8"))
        except (ValueError, TypeError):
            raise InvalidToken("Could not decode the given token")
        return data

    @staticmethod
    def _get_token_exp(token):
        return dt.datetime.utcfromtimestamp(_JWTAuth._decode_token(token)["exp"])
