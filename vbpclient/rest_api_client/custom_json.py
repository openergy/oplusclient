import json
import datetime as dt
from uuid import UUID
from collections import OrderedDict

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class _MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.strftime(ISO_FORMAT)
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return super().default(o)


def _json_str_to_o(s):
    try:
        return dt.datetime.strptime(s, ISO_FORMAT)
    except ValueError:
        return s


def _parse_dates(o):
    if isinstance(o, str):
        return _json_str_to_o(o)
    elif isinstance(o, dict):
        iterable = o.items()
    elif isinstance(o, list):
        iterable = enumerate(o)
    else:
        return o
    # is iterable
    for k, v in list(iterable):
        o[k] = _parse_dates(v)
    return o


def dumps(o, **kwargs):
    return json.dumps(o, cls=_MyJSONEncoder, **kwargs)


def dump(obj, fp, **kwargs):
    with open(fp, "w") as f:
        f.write(dumps(obj, **kwargs))


def loads(s, **kwargs):
    o = json.loads(s, object_pairs_hook=OrderedDict, **kwargs)
    return _parse_dates(o)


def load(fp, **kwargs):
    with open(fp) as f:
        return loads(f.read())
