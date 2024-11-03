import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

df = sns.load_dataset('mpg')

print(df.describe())

import sys
# sys.exit(0)

print(f'Количество строк {df.shape[0]} и столбцов {df.shape[1]}')

na_sum = df.isna().sum(axis=0)

print(f'Доля пропусков {sum(na_sum) / df.shape[0]:.2f}')


rows = df.shape[0]

df_num = df.select_dtypes(include='number')

# sys.exit(0)

# for col in df_num:
#     serie = df[col]
#     print(serie.isna().sum(axis=0) / rows)
#     print(serie.max(), serie.min())
#     print(serie.mean(), serie.std())
#     print(serie.var(), serie.median())
#     print(serie.quantile(0.1))
#     print(serie.quantile(0.9))

#     print(serie.quantile(0.25), serie.quantile(0.75))


# df_cat = df.select_dtypes(include='object')

# for col in df_cat:
#     serie = df[col]
#     print(len(serie.unique()))
#     print(f'{serie.isna().sum() / df.shape[0]:.2f}')
#     print(*serie.mode())


x = df.select_dtypes(include='object')

# print(x.describe().loc['count'])

# ax1 = plt.scatter(x=df['horsepower'],
                    #   y=df['mpg'],
                    #   c='DarkBlue')

df.plot.scatter(x = 'horsepower', y = 'mpg')




y = df['mpg'].to_numpy()
x = df['horsepower']
x.fillna(df['horsepower'].median(), inplace=True)
x = x.to_numpy()


print(df['horsepower'].isna().sum())

#GD
print(x.shape)
observations, *_ = x.shape

add_ = np.ones((observations, 1))

x = x.reshape(398, 1)

print(add_.shape, x.shape)

features = 1
lr = 0.05


weights = np.ones((features + 1, 1))

hist = [weights]


print(weights.shape)

# for iteration in range(50):
#     y_pred = a_n * X + b_n
#     error = y_pred - y
#     a_gradient = 2/m * np.sum(X * error)
#     b_gradient = 2/m * np.sum(error)
#     a_n = a_n - learning_rate * a_gradient
#     b_n = b_n - learning_rate * b_gradient
#     a_history.append(a_n)
#     b_history.append(b_n)

a = -0.1
b = 4

# x = 2 * np.random.rand(100, 1)
# y = 4 + 3 * x + np.random.randn(100, 1)

y = y.reshape(398, 1)


lr = 0.00008

# for i in range(500000):
#     y_pred = a * x + b
#     err = y_pred - y

#     # print(y_pred[:5], err[:5], np.sum(x * err))

#     a_gradient = 2 / observations * np.sum(x * err)
#     b_gradient = 2 / observations * np.sum(err)

#     # print(a_gradient, b_gradient)

# #     print(a_gradient)

#     a = a - lr * a_gradient
#     b = b - lr * b_gradient

#     # hist.append(a)

# print(a, b)


m = len(x)

a = 1
b = 1

lr = 0.00006

for i in range(200000):
    rand_index = np.random.randint(m)
    x_i = x[rand_index]
    y_i = y[rand_index]
    y_pred = a * x_i + b
    error = y_pred - y_i
    a_gradient = 2 * x_i * error
    b_gradient = 2 * error
    a = a - lr * a_gradient
    b = b - lr * b_gradient

    print(a, b)
    

    hist.append(a)
    # b_history.append(b_n)


# print(hist)

# x = np.linspace(0, 200)
# y = a * x + b

# plt.scatter(x = x, y = y)

# plt.show()



