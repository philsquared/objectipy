from dataclasses import dataclass
from typing import Optional

from objectipy.objectipy import dict_to_object


@dataclass
class Leaf:
    name: str
    age: int

@dataclass
class LeafWithOptional:
    name: str | None
    age: Optional[int]


def test_single_class():
    data = {
        "name": "Fred",
        "age": 42
    }
    leaf = dict_to_object(data, Leaf)
    assert leaf.name == "Fred"
    assert leaf.age == 42

def test_single_class_with_optionals():
    leaf = dict_to_object({}, LeafWithOptional)
    assert leaf.name is None
    assert leaf.age is None

    leaf = dict_to_object({"name": "Fred"}, LeafWithOptional)
    assert leaf.name == "Fred"
    assert leaf.age is None

    leaf = dict_to_object({"age": 42}, LeafWithOptional)
    assert leaf.name is None
    assert leaf.age == 42
