import types
import typing


def is_union(source_type: type) -> bool:
    origin = typing.get_origin(source_type)
    return origin is typing.Union or origin is types.UnionType


def is_list(source_type) -> bool:
    if isinstance(source_type, list):
        return True
    return issubclass(source_type, typing.List)


class NormalisedType:

    def __init__(self, source_type):
        # Remove any annotations
        origin_type = typing.get_origin(source_type)
        if origin_type is typing.Annotated:
            source_type = typing.get_args(source_type)[0]
            origin_type = typing.get_origin(source_type)

        if origin_type is typing.Union or origin_type is types.UnionType:
            self.outer_type = typing.Union
            self.inner_type = typing.get_args(source_type)
            return

        if isinstance(source_type, typing.List):
            self.outer_type = typing.List
            self.inner_type = source_type[0]
            return

        if ((origin_type and issubclass(origin_type, typing.List)) or
                issubclass(source_type, typing.List)):
            self.outer_type = typing.List
            inner_types = typing.get_args(source_type)
            if inner_types:
                self.inner_type = inner_types[0]
            else:
                self.inner_type = typing.Any
            return

        self.outer_type = source_type
        self.inner_type = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, NormalisedType):
            return False

        # Leaf type
        if other.inner_type is None:
            if other.outer_type is typing.Any or self.outer_type is typing.Any:
                return True
            return issubclass(self.outer_type, other.outer_type)

        if other.outer_type is typing.Union:
            for inner_type in other.inner_type:
                if NormalisedType(self.outer_type) == NormalisedType(inner_type):
                    return True
            return False

        if self.outer_type != other.outer_type:
            return False

        return NormalisedType(self.inner_type) == NormalisedType(other.inner_type)


def is_convertible(source_type, target_type) -> bool:
    return NormalisedType(source_type) == NormalisedType(target_type)


def is_optional(field_type: type) -> bool:
    if is_union(field_type):
        return type(None) in field_type.__args__
    else:
        return False

