def sort_func(f, args):
    return sorted(f(args))


def get_list(numbers_str: str) -> list:
    '''return list of integers from string'''
    return [int(i) for i in numbers_str.split()]


test_input_string = '12 1 89 55 37'

print(sort_func(get_list, test_input_string))