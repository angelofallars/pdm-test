"""Utilities for working with Pydantic."""

import asyncio
import logging
from typing import Final

from pydantic import ConfigDict, validate_call
from result import Err, Ok, Result

PYDANTIC_CONFIG: Final[ConfigDict] = ConfigDict(
    arbitrary_types_allowed=True,
    strict=True,
    validate_assignment=True,
)
"""Sensible configuration defaults for Pydantic models.

Reference: https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict
"""

validate = validate_call(config=PYDANTIC_CONFIG, validate_return=True)
"""A decorator around a function that validates the arguments and the return value.

Reference: https://docs.pydantic.dev/latest/concepts/validation_decorator/
"""

type Unit = tuple[()]

s: Unit = ()


def getter() -> Result[str, str]:
    return Ok("hi")


async def main() -> Result[None, str]:
    result = getter()
    if isinstance(result, Err):
        return Err(f"main: {result.err()}")
    item = result.ok()
    print(item)

    return Ok(None)


if __name__ == "__main__":
    match asyncio.run(main()):
        case Err(err):
            logging.fatal(err)
            exit(1)
        case Ok(_):
            exit(0)
