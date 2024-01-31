"""Utilities for working with Pydantic."""

from typing import Final

import pydantic
from pydantic import validate_call

PYDANTIC_CONFIG: Final[pydantic.ConfigDict] = {
    "arbitrary_types_allowed": True,
    "strict": True,
    "validate_assignment": True,
}
"""Sensible configuration defaults for Pydantic models.

Reference: https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict
"""

validate = validate_call(config=PYDANTIC_CONFIG, validate_return=True)
"""A decorator around a function that validates the arguments and the return value.

Reference: https://docs.pydantic.dev/latest/concepts/validation_decorator/
"""
