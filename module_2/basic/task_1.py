def get_sorted_values(*args) -> tuple:
    """get 3 numbers as strings, return then in order max, min, other"""

    assert (
        len(args) == 3
    ), f"Incorrect number of parameters, have to be 3, found {len(args)}"

    max_, other, min_ = sorted([int(i) for i in args], reverse=True)

    return max_, min_, other

class MyClass:
    def __init__(self):
        self._value = None
 
    @property
    def value(self):
        """This is 'value' property."""
        return self._value
 

class ImmutableClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # Используем __dict__ напрямую, чтобы избежать вызова __setattr__
            self.__dict__[key] = value

        print(self.__dict__)
        # Устанавливаем флаг, что инициализация завершена
        self._initialized = True

    def __setattr__(self, key, value):
        # Запрещаем изменять атрибуты, если инициализация уже завершена
        if getattr(self, '_initialized', False):
            raise AttributeError("Нельзя изменять значение атрибутов после инициализации")
        super().__setattr__(key, value)

# Пример использования
obj = ImmutableClass(_value="Alice", age=30)

import numpy as np

if __name__ == "__main__":

    arr1 = np.array([200, 250], dtype=np.uint8).reshape(-1, 1)
    arr2 = np.array([40, 40], dtype=np.uint8).reshape(-1, 1)
    add_numpy = arr1+arr2

    print(add_numpy)


    
    # numbers = (input() for i in range(3))

    # print(*get_sorted_values(*numbers), sep='\n')

    # print(hash(test))


    # test.__call__ = lambda x: x * 2


    # print(hash(test))
