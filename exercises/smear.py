import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

smear = pd.read_csv("../datasets/smear.csv", header=0, skiprows=range(1, 5))

smear.rename(columns={'Unnamed: 0': 'ts'}, inplace=True)
smear['ts'] = pd.to_datetime(smear['ts'])
smear = smear.set_index('ts')

df = pd.DataFrame(smear, index=smear.index)
df = df.resample("D", how={'t': np.mean, 'rmm': np.sum, 'dp': np.mean, 'rh': np.mean, 'p': np.mean, 'ws': np.mean, 'wdir': 'last'})
df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day

df = df.reindex_axis(df.columns[-3:].append(df.columns[:-3]), axis=1)

df.to_csv("../datasets/weather-kumpula.csv")
