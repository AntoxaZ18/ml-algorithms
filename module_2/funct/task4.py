from itertools import combinations


def get_combinations(s: str, k:int):
    res = []

    for i in range(2, k+1):
        res += [''.join(i) for i in combinations(s, i)]

    return res


test_input_string = 'строка'

print(get_combinations(test_input_string, 3))
