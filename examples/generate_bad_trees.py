import pandas as pd
import numpy as np
import scipy.stats as stats
import random

height = np.random.randint(13, 301, 900)
diam = np.round(height / 7 * (1 + np.sqrt(0.2) * np.random.randn(900)))
height = np.concatenate((height, [-9999 for _ in range(90)]))
height = np.concatenate((height, [None for _ in range(5)], ["E" for _ in range(5)]))
diam = np.concatenate((diam, [None for _ in range(100)]))
height[0] = 540

treeID = [str(x) for x in np.random.randint(100001, 300100, 1000)]
plotID = [x[:4] for x in treeID]
treeID = [x[-2:] for x in treeID]
species = stats.rv_discrete(values=([1, 3], [0.8, 0.3])).rvs(size=1000)
species[1] = 1.2

faketrees = pd.DataFrame()
faketrees['plotID'] = plotID
faketrees['treeID'] = treeID
faketrees['species'] = species
faketrees['height'] = height
faketrees['diam'] = diam

rows = random.sample(faketrees.index, faketrees.index.size)
faketrees = faketrees.ix[rows]
faketrees.to_csv("faketrees.csv", na_rep="")
