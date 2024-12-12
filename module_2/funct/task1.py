
def longer_3(s: str):
    return len(s) > 3

test_input_string = 'Уфа Москва Аша Казань'

long_names = [i for i in test_input_string.split() if longer_3(i)]

print(' '.join(long_names))
