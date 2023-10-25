from typing import Optional

from objectipy.utils import is_convertible, is_optional


def test_is_convertible():
    assert is_convertible(str, str)
    assert is_convertible(str, str | None)


def test_is_optional():
    assert is_optional(str | None)
    assert is_optional(None | str)
    assert is_optional(Optional[str])
