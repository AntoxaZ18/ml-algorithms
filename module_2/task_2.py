import pytest

def check_ticket(ticket: str) -> str:
    '''get ticket num as str of len 6 (example 789464) and 
    return Счастливый or Обычный if left and right sum are equal'''

    assert isinstance(ticket, str)

    assert len(ticket) == 6, f'Length of ticket {len(ticket)} is not correct, expected to be 6'

    if not ticket.isdigit():
        raise ValueError(f'{ticket} is not valid digit string')
       
    left_sum = sum(int(i) for i in ticket[:3])
    right_sum = sum(int(i) for i in ticket[3:])

    return 'Счастливый' if (left_sum == right_sum) else 'Обычный'



# print(check_ticket(input()))


def test_check_ticket():

    assert check_ticket('123456') == 'Обычный'
    assert check_ticket('123321') == 'Счастливый'


    with pytest.raises(AssertionError):  
        check_ticket('12332')

    with pytest.raises(AssertionError):  
        check_ticket('12332')

    with pytest.raises(AssertionError):  
        check_ticket(123456)

    with pytest.raises(ValueError):  
        check_ticket('123_46')



test_check_ticket()