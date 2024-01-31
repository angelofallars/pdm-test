"""An example of the Python programming standards."""

import math
import sys
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field, ValidationError
from result import Err, Ok, Result

# The Pi constant isn't declared here because Ruff told me to use math.pi
# instead. But if it were here it would look like:
#      PI: Final = 3.14

Color = Literal["red", "orange", "yellow", "green", "blue", "purple", "white", "gray", "black"]


class Square(BaseModel):
    """Represents a square.

    Attributes:
        kind: The kind of shape. Literal "square".
        color: The color of the shape.
        width: The width of the square.
    """

    kind: Literal["square"] = "square"
    color: Color
    width: float = Field(gt=0)  # gt=0 means accept only values greater than 0


class Rectangle(BaseModel):
    """Represents a rectangle.

    Attributes:
        kind: The kind of shape. Literal "rectangle".
        color: The color of the shape.
        width: The width of the square.
        height: The height of the square.
    """

    kind: Literal["rectangle"] = "rectangle"
    color: Color
    width: float = Field(gt=0)
    height: float = Field(gt=0)


class Circle(BaseModel):
    """Represents a circle.

    Attributes:
        kind: The kind of shape. Literal "circle".
        color: The color of the shape.
        radius: The radius of the circle.
    """

    kind: Literal["circle"] = "circle"
    color: Color
    radius: float = Field(gt=0)


Shape: TypeAlias = Square | Rectangle | Circle


def calculate_area(shape: Shape) -> float:
    """Calculates the area of a ``shape``.

    Params:
        shape: A shape.

    Returns:
        The area of a ``shape``.
    """
    match shape:
        case Square():
            return shape.width**2
        case Rectangle():
            return shape.width * shape.height
        case Circle():
            return math.pi * shape.radius**2


def calculate_perimeter(shape: Shape) -> float:
    """Calculates the perimeter of a ``shape``.

    Params:
        shape: A shape.

    Returns:
        The perimeter of a ``shape``.
    """
    match shape:
        case Square():
            return shape.width * 4
        case Rectangle():
            return (shape.width * 2) + (shape.height * 2)
        case Circle():
            return 2 * math.pi * shape.radius


def print_shape_info(shape: Shape):
    """Prints information about a ``shape``.

    Params:
        shape: A shape.
    """
    print(f"Shape of kind '{shape.kind}' and color '{shape.color}'")

    match shape:
        case Square():
            print(f"Width:     {shape.width}")
        case Rectangle():
            print(f"Height:    {shape.height}")
            print(f"Width:     {shape.width}")
        case Circle():
            print(f"Radius:    {shape.radius}")

    print(f"Perimeter: {calculate_perimeter(shape):.2f}")
    print(f"Area:      {calculate_area(shape):.2f}")
    print()


def main() -> Result[None, str]:
    """Main function of the program.

    Returns:
        Result with a string explaining the error.
    """
    white_rectangle = Rectangle(color="white", width=1, height=2)
    print_shape_info(white_rectangle)

    blue_circle = Circle(color="blue", radius=99)
    print_shape_info(blue_circle)

    try:
        orange_square = Square(color="orange", width=-2)
    except ValidationError as err:
        return Err(f"main: {err}")

    print_shape_info(orange_square)

    return Ok(None)


if __name__ == "__main__":
    match main():
        case Err(err):
            print(err, file=sys.stderr)
            exit(1)
        case Ok(_):
            exit(0)
