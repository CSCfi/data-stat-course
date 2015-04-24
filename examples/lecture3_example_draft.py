# Lecture 3 "Otherwise bad"
# Ok, you finally managed to read in the data and you have it on your workspace in a data frame
# What now?

import pandas as pd
import numpy as np
import pandas.rpy.common as com
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

# missing values: in R, the special symbol NA, in pandas...
# data types: in R (most important) numeric, factor, character, maybe boolean

letters = np.concatenate((com.load_data('letters'), [None]))
lettersS = pd.Series(letters)
lettersC = pd.Series(letters, dtype='category')
numbers = pd.Series(np.concatenate((range(1, 11), [np.nan])))
booleans = pd.Series([True, False])

fakedf = pd.DataFrame({
    'letterC': np.random.choice(lettersC, 300),
    'letterS': np.random.choice(lettersS, 300),
    'number': np.random.choice(numbers, 300),
    'bool': np.random.choice(booleans, 300),
})

fakedf.describe()
# take a summary of the whole data frame: this will show a summary of each of the columns
# XXX: With Pandas object columns are not summarized and the output is quite sparse compared to output
#      produced by R

# for numeric vector columns: 6 numbers describing the distribution (range, quartiles, mean)
# and the number of missing values

# for factors: frequencies of the (most common, if many) levels, and the number of missing values

# for character: not much

# for boolean: breakdown of values

# This will quickly show you if columns turn out to be of wrong type, or if the whole result is bogus.
# Compare:
iris = com.load_data('iris')
iris.to_csv("iris.csv")
print pd.read_csv("iris.csv").describe()
print pd.read_csv("iris.csv", sep=';', decimal=',').describe()

# Stuff happens! Take this cautionary tale for example
faketrees = pd.read_csv("faketrees.csv")  # everything looks normal
print faketrees.describe()
# wait, what? height should obviously be numeric but it seems to be a factor
# XXX: In case of Pandas, height column is missing
print faketrees.dtypes
# height has a type "object". How did this happen?

# summary on a single column gives more info:
print faketrees['height'].describe()

# For some reason these are not all numbers.
# (In this particular case, trees with two trunks etc. had a letter code in place of height.)
# Therefore, read_csv concludes that it's not numeric, but character, which are by default
# changed objects.

# On top of that, some values are actually missing, and other missing values are marked with -9999

# Ways to deal with this:
# declare all the stupid values as missing (not always plausible):
faketrees = pd.read_csv("faketrees.csv", na_values=["-9999", "E"])
faketrees.describe(include='all')

# The other way around: from numeric to a Categorical
faketrees['speciesf'] = pd.Categorical(faketrees['species'], categories=[1, 3]).rename_categories(['pine', 'spruce']) 
faketrees.describe(include='all')

# more ways to look at missing values
# is.na(fakedf$number)
# sum(complete.cases(fakedf)) #how many rows have no missing values

np.sum(pd.isnull(fakedf['number']))

# Outliers: values can be of the correct type but still completely wrong, or just odd
# total outliers will show up nicely in a histogram or a boxplot

faketrees['height'].hist()
faketrees['height'].plot(kind='box')

# what should you do with outliers is another question entirely

# barplots are nice for frequencies of categorical data
pd.value_counts(faketrees['species'], normalize=True).plot(kind='bar')
pd.value_counts(np.asarray(faketrees['speciesf']), normalize=True).plot(kind='bar')

# more quick and dirty ways to explore data visually:
# scatterplots of two continuous variables
faketrees.plot(kind='scatter', x='diam', y='height')

# boxplots by category
faketrees.boxplot(column=['height'], by=['speciesf'])

