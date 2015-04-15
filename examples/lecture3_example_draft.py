# Lecture 3 "Otherwise bad"
# Ok, you finally managed to read in the data and you have it on your workspace in a data frame
# What now?

import pandas as pd
import numpy as np

# missing values: in R, the special symbol NA, in pandas...
# data types: in R (most important) numeric, factor, character, maybe boolean

letters = [chr(x + ord('a')) for x in range(26)]
letters.append(None)
lettersSeries = pd.Series(letters)
lettersCategory = pd.Series(letters, dtype='category')
numbers = pd.Series(np.concatenate((range(1, 11), [np.nan])))
booleans = pd.Series([True, False])

fakedf = pd.DataFrame({
    'letterCategory': lettersCategory.iloc[np.random.choice(lettersCategory.index, 300)],
    'letterSeries': lettersSeries.iloc[np.random.choice(lettersSeries.index, 300)].reset_index()[0],
    'number': numbers.iloc[np.random.choice(numbers.index, 300)].reset_index()[0],
    'bool': booleans.iloc[np.random.choice(booleans.index, 300)].reset_index()[0],
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
iris = pd.read_csv('https://raw.github.com/pydata/pandas/master/pandas/tests/data/iris.csv')
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
print faketrees.describe()
# read in as pure character, deal with it manually
# faketrees<-read.csv("faketrees.csv",as.is=TRUE)
# faketrees$heightn<-as.numeric(faketrees$height)
# the warning message from that is to be expected and is allright, compare:
# as.numeric(c("1","345.9","foo","8"))
# faketrees$heightn<-ifelse(faketrees$heightn>0,faketrees$heightn,NA)
# "if heightn is positive, leave it as it is, else mark it as missing

# The other way around: from numeric to a factor
# faketrees$speciesf<-factor(faketrees$species,labels=c("pine","spruce"))
# uh oh! what now? it was supposed to be just 1's and 2's
# table(faketrees$species)
# or, maybe also
# levels(as.factor(faketrees$species))
# one way to deal with this:
# faketrees$speciesf<-factor(faketrees$species,levels=1:2,labels=c("pine","spruce"))
# summary(faketrees)
# the extra levels become NA

# more ways to look at missing values
# is.na(fakedf$number)
# sum(complete.cases(fakedf)) #how many rows have no missing values

# Outliers: values can be of the correct type but still completely wrong, or just odd
# total outliers will show up nicely in a histogram or a boxplot
# hist(faketrees$heightn)
# boxplot(faketrees$heightn)
# what should you do with outliers is another question entirely

# barplots are nice for frequencies of categorical data
# barplot(table(faketrees$species)) #the extra problem category is evident
# barplot(table(faketrees$speciesf))
# in fact this can be done even simpler with a genuine factor
# plot(faketrees$speciesf)

# more quick and dirty ways to explore data visually:
# scatterplots of two continuous variables
# plot(heightn~diam,data=faketrees) #remember this is artificial data!
# boxplots by category
# boxplot(heightn~speciesf,data=faketrees) #still... the populations are equal
