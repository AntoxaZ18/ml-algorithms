from string import ascii_lowercase,ascii_uppercase
from random import choice


def gen_password(length = 12):
    '''generate password with given length'''
    chars = ascii_lowercase + ascii_uppercase + "0123456789!?@#$*"

    while True:
        yield ''.join((choice(chars) for _ in range(length)))