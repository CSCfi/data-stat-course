#Simple frequencies by group: barplot
import scipy
import numpy as np
import pandas as pd
from ggplot import *
import matplotlib.pyplot as plt


letters_df = pd.read_csv('../datasets/letters.csv')
letters = np.array(letters_df['small'])
LETTERS = np.array(letters_df['capital'])

xk = np.arange(5)
pk = (0.1, 0.2, 0.25, 0.4, 0.05)
idxs = scipy.stats.rv_discrete(values=(xk, pk)).rvs(size=100)

tmp = pd.DataFrame()
tmp['idxs'] = idxs
tmp['group'] = LETTERS[idxs]
plt.figure()
pd.value_counts(tmp['group'], normalize=True).plot(kind='bar')
plt.show()

#Cross tabulations of frequencies by two groupings:
#stacked or grouped barplots
tmp['anothergroup'] = letters[np.random.randint(23, 26, 100)]
pd.crosstab(tmp['group'], tmp['anothergroup']).plot(kind='bar')

tmp['xvar'] = tmp['idxs'] * np.random.randn(100)
tmp[['group', 'xvar']].groupby('group').boxplot()

mt = pd.read_csv("monthtemps.csv")
mt.reindex(np.random.permutation(mt.index))
mt['NNf'] = pd.Series(mt['NordklimNumber'], dtype="category")
ggplot(mt, aes('month', 'tempmean')) + geom_point(colour='steelblue')
ggplot(mt, aes('month', 'tempmean')) + geom_point(colour='steelblue') +facet_wrap("NNf")

x = np.linspace(0,10,50)
y = 2.5 * x + 1.2
noise = np.random.randn(y.size)
noisy = y + noise
p = np.polyfit(x,noisy,1)
plt.plot(x, noisy, 'b.')
plt.plot(x, p[0] * x + p[1],'r-')


