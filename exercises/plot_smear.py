import pandas as pd
import matplotlib.pyplot as pl

smear = pd.read_csv(
    "../datasets/weather-kumpula.csv",
    header=0,
    index_col=0,
    parse_dates=True)

df = pd.DataFrame(smear)
pl.figure()
ax1 = df.t.plot(style='r-', legend=False, title="Weather 2014 (Kumpula, Helsinki)")
ax2 = df.rmm.plot(secondary_y=True, style='b.')
ax1.set_ylabel("average temperature per day (celcius)")
ax2.right_ax.set_ylabel("cumulated rainfall per day (mm)")
pl.savefig("foo.png")
