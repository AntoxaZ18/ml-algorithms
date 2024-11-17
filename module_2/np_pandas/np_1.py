import numpy as np

arr = np.ones(64).reshape(8, 8)

arr[::2, ::2] = 0
arr[1::2, 1::2] = 0

n = 5
stdev = np.sqrt(n)

arr_random = np.random.normal(scale = stdev, size = 2000000)

print(arr_random.mean())
print(arr_random.var())


