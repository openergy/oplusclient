from .models import BaseModel


# fixme: should be used everywhere
def get_id(record_or_dict_or_id):
    if isinstance(record_or_dict_or_id, str):
        return record_or_dict_or_id
    if isinstance(record_or_dict_or_id, dict):
        return record_or_dict_or_id["id"]
    if isinstance(record_or_dict_or_id, BaseModel):
        return record_or_dict_or_id.id
    raise TypeError(f"wrong type for record_or_dict_or_id: {type(record_or_dict_or_id)}")
