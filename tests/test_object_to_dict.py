from dataclasses import dataclass

from objectipy.objectipy import object_to_dict

@dataclass
class A:
    a: int = 42
    b: str = "hello"
    c: str | None = None


def test_object_to_dict():
    a = A()
    assert object_to_dict(a) == {"a": 42, "b": "hello"}
    assert object_to_dict(a, exclude_none=False) == {"a": 42, "b": "hello", "c": None}
    assert object_to_dict(a, exclude=["b"]) == {"a": 42}
    assert object_to_dict(a, exclude=["a", "b"]) == {}
    assert object_to_dict(a, exclude=["b"], exclude_none=False) == {"a": 42, "c": None}

    assert object_to_dict(a, include=["a"]) == {"a": 42}
    assert object_to_dict(a, include=["b"]) == {"b": "hello"}
    assert object_to_dict(a, include=["a", "b"]) == {"a": 42, "b": "hello"}
    assert object_to_dict(a, include=["a", "b"], exclude=["b"]) == {"a": 42}

