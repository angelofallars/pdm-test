from typing import Protocol


class Error(Protocol):
    def error(self) -> str: ...


type E = list[int]


class _WrappedError:
    message: str
    err: Error
