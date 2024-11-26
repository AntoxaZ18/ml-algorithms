import pytest
from random import randint, choice, uniform
from operator import truediv, mul, sub, add
import cmath

from complex import ComplexNumber
def test_sorted():

    TEST_NUMS = 10000

    operators = (sub, add, truediv, mul)

    for _ in range(TEST_NUMS):
        x1 = uniform(0, 100)
        y1 = uniform(0, 100)

        x2 = uniform(0, 100)
        y2 = uniform(0, 100)
        op = choice(operators)
        assert op(ComplexNumber(x1, y1), ComplexNumber(x2, y2)) == op(complex(x1, y1), complex(x2, y2))


    for _ in range(TEST_NUMS):
        x1 = uniform(0.1, 100)
        y1 = uniform(0.1, 100)

        x, y = ComplexNumber(x1, y1).polar()

        b = ComplexNumber(x, y, form='polar')

        assert cmath.isclose(x1, b.real) is True
        assert cmath.isclose(y1, b.imag) is True

    with pytest.raises(ValueError):
        x = ComplexNumber(1, 'z_19')

    with pytest.raises(ValueError):
        x = ComplexNumber(5.2, 6.5, form='not polar')

