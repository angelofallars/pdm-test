from typing import Protocol, runtime_checkable

from dvutil import validate
from pydantic.dataclasses import dataclass
from result import Ok, Result


@runtime_checkable
class HasID(Protocol):
    """A protocol that accepts objects with an ``id`` instance variable/property."""

    @property
    def id(self) -> str:
        """The ID that represents the object."""
        ...

    @id.setter
    def id(self, new_id: str) -> None:
        ...


@validate
def print_id(value: HasID):
    print(f"ID of object: {value.id}")


@validate
def set_id(value: HasID):
    value.id = "NEW ID"


@validate
def should_return_result() -> Result[str, str]:
    return Ok("heeee")


@dataclass
class Person:
    id: str
    name: str
    age: int


class EatEat:
    _id: str

    def __init__(self) -> None:
        self._id = "EatEatEat"

    @property
    def id(self) -> str:
        return "eee"

    @id.setter
    def id(self, new_id: str):
        self._id = new_id


print_id(Person("823480uu", "Alec", 24))

person = Person("eeoirsnta", "Alice", 19)

print(person)
set_id(person)
print(person)

print_id(EatEat())
