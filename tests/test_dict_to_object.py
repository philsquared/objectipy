from dataclasses import dataclass
from typing import Optional

from objectipy import dict_to_object


@dataclass
class Leaf:
    name: str
    age: int

@dataclass
class LeafWithOptional:
    name: str | None
    age: Optional[int]


@dataclass
class Node:
    height: int
    leaf: Leaf

@dataclass
class HasColour:
    colour: str


def dict_to_object2(data: dict, cls: type, allow_extra_data=False):
    return dict_to_object(data, cls, allow_extra_data=allow_extra_data)


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


def test_extra_data_single():
    data = {
        "name": "Fred",
        "age": 42,
        "colour": "Red"
    }
    leaf = dict_to_object(data, Leaf, allow_extra_data=True)
    assert data.get("colour") == "Red"
    assert leaf.name == "Fred"
    assert leaf.age == 42


def test_extra_data_multi():
    data = {
        "height": 7,
        "leaf": {
            "name": "Fred",
            "age": 42
        },
        "colour": "Red"
    }
    node = dict_to_object(data, Node, allow_extra_data=True)
    assert node.height == 7
    assert node.leaf.name == "Fred"
    assert node.leaf.age == 42
    assert data.get("colour") == "Red"

    has_colour = dict_to_object(data, HasColour)
    assert has_colour.colour == "Red"
