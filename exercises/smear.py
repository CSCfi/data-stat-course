import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

# -> ts valmiiksi luettavaan muotoon
# -> valmiiksi päiväkohtaisesti aggretoitu

smear = pd.read_csv("../datasets/smear.csv", header=0, skiprows=range(1, 5))

smear.rename(columns={'Unnamed: 0': 'ts'}, inplace=True)
smear['ts'] = pd.to_datetime(smear['ts'])
smear = smear.set_index('ts')

df = pd.DataFrame(smear, index=smear.index, columns=('t', 'rmm'))
df = df.resample("D", how={'t': np.mean, 'rmm': np.sum})

ax1 = df.t.plot(style='r-', legend=False, title="Weather 2014 (Kumpula, Helsinki)")
ax2 = df.rmm.plot(secondary_y=True, style='b.')
ax1.set_ylabel("average temperature per day (celcius)")
ax2.right_ax.set_ylabel("cumulated rainfall per day (mm)")
pl.show()
