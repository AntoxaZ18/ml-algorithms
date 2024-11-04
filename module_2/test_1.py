from task_1 import get_sorted_values
import pytest


def test_sorted():

    assert get_sorted_values(19, 89, 5) == (89, 5, 19)

    with pytest.raises(AssertionError):
        get_sorted_values(1, 19, 22, 59)

    with pytest.raises(ValueError):
        get_sorted_values(1, 'z_19', 22)
