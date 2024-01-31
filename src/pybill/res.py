import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, override

from pydantic.dataclasses import dataclass
from result import Err, Ok, Result

if TYPE_CHECKING:
    import pathlib


def accept_iter[T](it: Iterable[T]):
    for i in it:
        print(i)


@dataclass
class Item:
    id: str
    name: str


class ErrNotFound: ...


class ErrAlreadyExists: ...


class HasID(Protocol):
    id: str


T = TypeVar("T", bound=HasID)


class CRUDRepository(ABC, Generic[T]):
    """An abstract repository for CRUD operations on one entity."""

    @abstractmethod
    def create(self, entity: T) -> Result[None, ErrAlreadyExists]:
        """Creates an item.

        Args:
            entity: The entity object.

        Returns:
            Result of the create operation.
        """

    @abstractmethod
    def read(self, id: str) -> Result[T, ErrNotFound]:
        """Tries to fetch an entity using the given id and returns the entity if found.

        Args:
            id: The ID of the entity.

        Returns:
            Result with the entity object.
        """

    @abstractmethod
    def update(self, entity: T) -> Result[None, ErrNotFound]:
        """Updates an item.

        Args:
            entity: The entity object.

        Returns:
            Result of the update operation.
        """

    @abstractmethod
    def delete(self, id: str) -> Result[None, ErrNotFound]:
        """Deletes an item.

        Args:
            id: The ID of the entity.

        Returns:
            Result of the delete operation.
        """


ItemRepository = CRUDRepository[Item]
"""An abstract repository for items."""


class SQLiteItemRepository(ItemRepository):
    """A concrete SQLite repository for items."""

    _conn: sqlite3.Connection
    """The SQLITE3 connection that this repository is connected to."""

    def __init__(self, connection: sqlite3.Connection):
        """Initializes a new SQLiteItemRepository.

        Args:
            connection: The SQLite3 connection that this repository is connected to.
        """
        self._conn = connection

    @override
    def create(self, entity: Item) -> Result[None, ErrAlreadyExists]:
        try:
            cur = self._conn.cursor()
            _ = cur.execute(
                "INSERT INTO items VALUES(?, ?)",
                (
                    entity.id,
                    entity.name,
                ),
            )
            self._conn.commit()
        except sqlite3.Error as _:
            return Err(ErrAlreadyExists())

        return Ok(None)

    @override
    def read(self, id: str) -> Result[Item, ErrNotFound]: ...

    @override
    def update(self, entity: Item) -> Result[None, ErrNotFound]: ...

    @override
    def delete(self, id: str) -> Result[None, ErrNotFound]: ...


def handle_get_item_by_id(repo: ItemRepository) -> Result[Item, str]:
    id: object = "22"

    match repo.read(id):
        case Err(e):
            return Err(str(e))
        case Ok(item):
            item = item

    return Ok(item)


def my_function(j: "pathlib.Path"):
    print(j)


repo = SQLiteItemRepository(sqlite3.connect("Hello"))

res = repo.delete("hii")
