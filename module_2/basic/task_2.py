
def check_ticket(ticket: str) -> str:
    '''get ticket num as str of len 6 (example 789464) and 
    return "Счастливый" or "Обычный" if left and right sum are equal'''

    assert isinstance(ticket, str)

    assert len(ticket) == 6, f'Length of ticket {len(ticket)} is not correct, expected to be 6'

    if not ticket.isdigit():
        raise ValueError(f'{ticket} is not valid digit string')
      
    left_sum = sum(int(i) for i in ticket[:3])
    right_sum = sum(int(i) for i in ticket[3:])

    return 'Счастливый' if (left_sum == right_sum) else 'Обычный'


if __name__ == '__main__':
    print(check_ticket(input()))
