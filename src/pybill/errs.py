from typing import List, Protocol


class Error(Protocol):
    def error(self) -> str:
        ...


type e = List[int]


class _WrappedError:
    message: str
    err: Error
