import pandas as pd
import os
import matplotlib.pyplot as plt

TRUNC_CSV = 'trunc.csv'

if not os.path.exists(TRUNC_CSV):
    print('downloading dataframe')
    df = pd.read_csv('https://www.geos.ed.ac.uk/~weather/jcmb_ws/JCMB_2018_Mar.csv')
    df[:1000].to_csv(TRUNC_CSV)
else:
    df = pd.read_csv(TRUNC_CSV)


# df.drop(df.index[[0,]])



# df.columns = df.iloc[0]


r = df.iloc[1].fillna('')


t = df.iloc[0].astype(str)

r = t + ' ' + r

df.columns = r
df = df.drop(df.index[[0,1,2]])

df = df.reset_index(drop=True)

# print(df.head(20))

# print(df.tail(20))

# print(df[10:30])


df['Wavg_Avg m/s'] = df['Wavg_Avg m/s'].astype(float)


# largest_ms = df['Wavg_Avg m/s'].nlargest(10)
# largest_ms = largest_ms.reset_index(drop=True)


# largest_ms.plot()

# plt.show()

unique_relative_humidity = df['RHum_Avg %'].unique()

print(unique_relative_humidity, len(unique_relative_humidity))


# print(df['Wavg_Avg m/s'].nlargest(10))

