import dataclasses
from typing import Optional, Union, Annotated, get_type_hints, List

from objectipy.objectipy import is_convertible, is_optional

@dataclasses.dataclass
class ClassWithList:
    x: [str]
    x2: List[str]


def test_is_convertible():
    assert is_convertible(str, str)
    assert is_convertible(str, str | None)
    assert is_convertible(int, Optional[int])
    assert is_convertible(int, Union[str, Optional[int]])
    assert is_convertible(int, Annotated[Union[str, Optional[int]], "Hello"])

    hints = get_type_hints(ClassWithList)
    assert is_convertible(type(["a", "b"]), hints["x"])
    assert is_convertible(type(["a", "b"]), hints["x2"])


def test_is_optional():
    assert is_optional(str | None)
    assert is_optional(None | str)
    assert is_optional(Optional[str])

