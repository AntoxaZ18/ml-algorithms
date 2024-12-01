from typing import Iterable


class CyclicIterator:
    """class providing inifinte values from given iterable object"""

    def __init__(self, iterable: Iterable):
        self._iterable = iterable
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        ret_val = self._iterable[self._index % len(self._iterable)]
        self._index += 1
        return ret_val
