from task_2 import check_ticket
import pytest


def test_check_ticket():

    assert check_ticket('123456') == 'Обычный'
    assert check_ticket('123321') == 'Счастливый'
# 
    with pytest.raises(AssertionError):
        check_ticket('12332')

    with pytest.raises(ValueError):
        check_ticket('12_321')