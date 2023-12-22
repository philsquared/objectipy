import types
import typing


def is_union(source_type: type) -> bool:
    origin = typing.get_origin(source_type)
    return origin is typing.Union or origin is types.UnionType


def is_convertible(source_type, target_type: type) -> bool:
    if is_union(target_type):
        return source_type in target_type.__args__
    else:
        return source_type == target_type


def is_optional(field_type: type) -> bool:
    if is_union(field_type):
        return type(None) in field_type.__args__
    else:
        return False
