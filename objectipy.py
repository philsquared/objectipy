from dataclasses import fields

from objectipy.secret import secret
from objectipy.utils import is_optional, is_convertible


def dict_to_object(data: dict, cls: type):
    try:
        mapping = cls._field_map() # !TBD check that it's a dict of strings
    except:
        mapping = {}
        pass

    def map_field_name(name: str) -> str:
        return mapping.get(name) or name

    for field in fields(cls):
        obj_field_name = field.name
        dict_name = map_field_name(obj_field_name)
        value = data.get(dict_name)
        if value is not None:
            if is_convertible( type(value), field.type ):
                pass
            elif field.type == secret and isinstance(value, str):
                data[dict_name] = secret(value)
            elif isinstance(value, dict):
                obj = dict_to_object(value, field.type)
                data[dict_name] = obj
            else:
                raise Exception(f"field '{dict_name}' expected type: {field.type} but found {type(value)}")
        else:
            if is_optional(field.type):
                data[dict_name] = None
            else:
                raise Exception(f"Missing value for field '{dict_name}'")
        if obj_field_name != dict_name:
            data[obj_field_name] = data[dict_name]
            del data[dict_name]

    return cls(**data)
