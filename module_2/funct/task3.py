from itertools import permutations


def get_permutations(s: str, k:int):
    return sorted([''.join(i) for i in (list(permutations(s, k)))])


test_input_string = 'строка'

print(get_permutations(test_input_string, 3))
