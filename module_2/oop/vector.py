from __future__ import annotations
from math import sqrt, isclose
from typing import Iterable, Union
from typing_extensions import Self


class Vector(tuple):
    """class for representin N dimnesion vector based on tuple container.
    support operations (add, radd, sub, rmul, mul on scalar and another vector, gt, ge operators (comoare length of vectors))
    functions for calculating length vector, cosine between vectors and eudclide metric"""

    def validate_vector(self, other_vector: Vector) -> None:
        """validate argument for operation check isinstance and shape of vectors"""

        if not isinstance(other_vector, self.__class__):
            raise TypeError(
                f"This operation alowed only with another Vector, found {type(other_vector)}"
            )

        if len(self) != len(other_vector):
            raise ValueError(
                f"Vector must have the same dimensions current {len(self)}, another {len(other_vector)}"
            )

    def __new__(cls, coords: Iterable[float]) -> tuple:
        # validate that all component of iterable are numbers
        if not all((isinstance(i, (float, int)) for i in coords)):
            raise TypeError("Vector must have coordinates only of types float and int")
        return super().__new__(cls, coords)

    def __add__(self, other: Vector) -> Self:
        self.validate_vector(other)
        return Vector(tuple(x + y for x, y in zip(self, other)))

    def __radd__(self, other: Vector) -> Self:
        self.validate_vector(other)
        return Vector(tuple(x + y for x, y in zip(self, other)))

    def __sub__(self, other: Vector) -> Self:
        self.validate_vector(other)
        return Vector(tuple(x - y for x, y in zip(self, other)))

    def __rmul__(self, other: Union[float, Vector]) -> Self:
        if not isinstance(other, (float, int, Vector)):
            raise TypeError("Arg must be only Vector, int or float")

        return self.__mul__(other)

    def __mul__(self, other: Union[float, Vector]) -> Self:
        if isinstance(other, (int, float)):
            return Vector(tuple(x * other for x in self))

        self.validate_vector(other)

        return sum((x * y for x, y in zip(self, other)))

    def __bool__(self) -> bool:
        return not all((isclose(x, 0) for x in self))

    def __eq__(self, other: Vector) -> bool:
        self.validate_vector(other)
        return all((isclose(a, b) for a, b in zip(self, other)))

    def __gt__(self, other: Vector) -> bool:
        """compare length of vectors"""
        self.validate_vector(other)
        return self.module() > other.module()

    def __ge__(self, other: Vector) -> bool:
        """compare length of vectors"""
        self.validate_vector(other)
        return self.module() >= other.module()

    def __le__(self, other: Vector) -> bool:
        """compare length of vectors"""
        self.validate_vector(other)
        return self.module() <= other.module()

    def __lt__(self, other: Vector) -> bool:
        """compare length of vectors"""
        self.validate_vector(other)
        return self.module() < other.module()

    def module(self) -> float:
        """return vector length with formula √sum(ai^2)"""
        return sqrt(sum(a * a for a in self))

    def cos(self, other: Vector) -> float:
        """cos of two ndim vectors with formula: cos(A) = ((a, b) / (|a| * |b|)"""

        self.validate_vector(other)

        if not other:
            raise ValueError(f"Cannot find cos with zero vector: {other}")
        return self * other / (self.module() * other.module())

    def euclide_dist(self, other: Vector) -> float:
        """calc euclidean distance of twi vectors using formula: √sum(ai−bi)^2"""
        self.validate_vector(other)

        return sqrt(sum((a - b) ** 2 for (a, b) in zip(self, other)))

    def __str__(self) -> str:
        return f"{len(self)} dim vec {tuple(self)}"
