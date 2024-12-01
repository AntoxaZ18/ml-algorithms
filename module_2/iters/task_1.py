from typing import Iterable


def task_process(lst: Iterable):
    """function for implement task"""
    if not isinstance(lst, Iterable):
        raise TypeError("lst must be a Iterable class [list, set...]")

    if not all((isinstance(i, (int, float)) for i in lst)):
        raise ValueError("lst must contain only numbers int or float")

    if not any((x > 0 for x in lst)):
        raise ValueError("lst must at least contain one positive number")

    return sorted(lst)
