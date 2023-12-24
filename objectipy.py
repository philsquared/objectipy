import inspect
import typing
from dataclasses import fields, dataclass, field
from typing import get_type_hints, Any

try:
    from .secret import Secret
    from .utils import is_optional, is_convertible
except:
    from secret import Secret
    from utils import is_optional, is_convertible


@dataclass
class Binding:
    name: str
    type_hint: type
    default_value: Any

    @property
    def is_optional(self):
        return self.default_value is not None or is_optional(self.type_hint)


def make_binding(name: str, type_hint: type, default_value: Any) -> Binding:
    if default_value is None:
        origin_type = typing.get_origin(type_hint)
        if inspect.isclass(origin_type) and issubclass(origin_type, typing.List):
            default_value = []
    return Binding(name, type_hint, default_value)

def dict_to_object(data: dict, cls: type, allow_extra_data=False):
    try:
        mapping = cls._field_map() # !TBD check that it's a dict of strings
    except:
        mapping = {}

    def map_field_name(name: str) -> str:
        return mapping.get(name) or name

    # Get all standard fields (non defaulted)
    bindings = {field.name: make_binding(field.name, field.type, None) for field in fields(cls)}
    hints = get_type_hints(cls)

    # Get fields with default values and mix in any type hints
    cls_fields = [(name, value) for name, value in cls.__dict__.items() if not name.startswith("__")]
    for name, value in cls_fields:
        type_hint = hints.get(name)
        if type_hint:
            bindings[name] = make_binding(name, type_hint, value)

    dict_fields = set(data.keys())
    for binding in bindings.values():
        obj_field_name = binding.name
        dict_name = map_field_name(obj_field_name)
        value = data.get(dict_name)
        if value is not None:
            if is_convertible(type(value), binding.type_hint):
                pass
            elif binding.type_hint == Secret and isinstance(value, str):
                data[dict_name] = Secret(value)
            elif isinstance(value, dict):
                obj = dict_to_object(value, binding.type_hint)
                data[dict_name] = obj
            else:
                raise Exception(f"field '{dict_name}' expected type: {binding.type_hint} but found {type(value)}")
            dict_fields.remove(dict_name)
        else:
            if binding.is_optional:
                data[dict_name] = binding.default_value
            else:
                raise Exception(f"Missing value for field '{dict_name}'")
        if obj_field_name != dict_name:
            data[obj_field_name] = data[dict_name]
            del data[dict_name]

    # Check if there are any outstanding fields
    if len(dict_fields) > 0:
        if allow_extra_data:
            this_data = {}
            extra_data = {}
            for k, v in data.items():
                if k in dict_fields:
                    extra_data[k] = v
                else:
                    this_data[k] = v
            for k in this_data.keys():
                del data[k]
            return cls(**this_data)
    return cls(**data)
