
def get_sorted_values(*args):
    '''get 3 numbers as strings, return then in order max, min, other'''

    assert len(args) == 3, f'Incorrect number of parameters, have to be 3, found {len(args)}'

    max_, other, min_ = sorted([int(i) for i in args], reverse=True)

    return max_, min_, other


numbers = (input() for i in range(3))

print(*get_sorted_values(*numbers), sep='\n')



