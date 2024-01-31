import asyncio
import os
from collections.abc import Callable
from typing import Final, ParamSpec, TypeVar

from result import Err, Ok, Result, as_result

DEFAULT_PORT: Final = 3000


def network_op() -> Result[int, str]:
    if 2 == 25:
        return Err("eeee")
    else:
        return Ok(24)


def call_result():
    res = network_op()

    if isinstance(res, Err):
        return
    res.unwrap()


async def main() -> int:
    print("Hello world!")
    return 0


def hello(e: str) -> int:
    if e == 2:
        return 2
    else:
        return 24


P = ParamSpec("P")
P2 = ParamSpec("P2")
R = TypeVar("R")
R2 = TypeVar("R2")


def catch_all(f: Callable[P, R]):
    return as_result(Exception)(f)


open = catch_all(os.open)
match open("./hello", 511):
    case Err(err):
        match err:
            case BaseException():
                ...
            case _:
                ...
    case Ok(f):
        ...


def cast_params(_: Callable[P, R]):
    def decorator(actual_fn: Callable[P2, R2]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return actual_fn(*args, **kwargs)  # pyright: ignore

        return wrapper

    return decorator


@cast_params(os.open)
def wrapped(): ...


class Firebase:
    get_collection = cast_params(os.open)(lambda x: x)


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def multiply(self):
        self.x = self.x * 2
        self.y = self.x * 2


my_point = Point(2, 3)

my_point.x = 2.4

if __name__ == "__main__":
    exit(asyncio.run(main()))
