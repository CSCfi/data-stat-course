#Simple frequencies by group: barplot
from scipy import stats
import pandas.rpy.common as com
import matplotlib.pyplot as plt

LETTERS = com.load_data('LETTERS')
letters = com.load_data('letters')

xk = np.arange(5)
pk = (0.1, 0.2, 0.25, 0.4, 0.05)
idxs = stats.rv_discrete(values=(xk, pk)).rvs(size=100)
tmp = pd.DataFrame()
tmp['group'] = LETTERS[idxs]
plt.figure()
pd.value_counts(tmp['group'], normalize=True).plot(kind='bar')
plt.show()

#Cross tabulations of frequencies by two groupings:
#stacked or grouped barplots
tmp['anothergroup'] = letters[np.random.randint(23, 26, 100)]
pd.crosstab(tmp['group'], tmp['anothergroup']).plot(kind='bar')

mt = pd.read_csv("monthtemps.csv")
mt.reindex(np.random.permutation(mt.index))
mt['NNf'] = pd.Series(mt['NordklimNumber'], dtype="category")
ggplot(mt, aes('month', 'tempmean')) + geom_point(colour='steelblue')
ggplot(mt, aes('month', 'tempmean')) + geom_point(colour='steelblue') +facet_wrap("NNf")

