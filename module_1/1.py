import numpy as np
import sys
from scipy.stats import lognorm
from functools import partial
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)

loc = 0
scale = 5
s = 0.5


rv = lognorm(loc = loc, scale = scale, s = s)



x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)
y = rv.pdf(x)
ax.plot(x, y, 'k-', lw=2, label='frozen pdf')


quant_10 = rv.ppf(0.1)
ax.vlines(quant_10, 0, max(y), color='k', linestyle='-', lw=1)

print(f'Время безотказной работы с вероятностью 0,9: {quant_10}')
print(rv.pdf(quant_10))


print(f'Мат ожидание {rv.mean()} Дисперсия: {rv.var()}')


plt.show()

