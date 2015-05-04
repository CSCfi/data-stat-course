# Lecture 4: "more wrangling"

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


# Just a reminder, adding new variables to data frames is easy, for example:
iris = pd.read_csv('../datasets/iris.csv')
iris.columns

iris['Sepal.Area'] = iris['Sepal.Length'] * iris['Sepal.Width']
iris.columns

# Replacing whole columns works the same way.
# To remove a single column DataFrame objects have drop method, which returns a *new*
# DataFrame with the chosen column dropped
iris2 = iris.drop('Sepal.Area', 1)
iris2.columns
iris.columns

# The column may be removed from a DataFrame object with del statement
del iris['Sepal.Area']
iris.columns

# loc:  label based indexing
# iloc: integer based indexing:
# XXX: Remember, indexing starts from zero, ":" selects whole axis
iris.iloc[:, :5] #pick just the first 5 columns

# By negative column index:
iris.iloc[:, :-1] #pick everything but the last column

# By column name:
iris.loc[:, ["Sepal.Length","Sepal.Width","Petal.Length","Petal.Width","Species"]]

# Unfortunately, negative column names don't work, and there are no inverse matching.
iris['Sepal.Area'] = iris['Sepal.Length'] * iris['Sepal.Width']
cols = iris.columns.tolist()  # list of column names
cols.remove('Sepal.Area')
iris.loc[:, cols]

# Binning, or making a continuous variable in to a discrete one
# Let's make a histogram of the sepal lengths
iris['Sepal.Length'].hist()
plt.show()

print "Values for Sepal.Length range from %s to %s" % (iris['Sepal.Length'].min(), iris['Sepal.Length'].max())
iris['SepalLengthGroup'] = pd.cut(iris['Sepal.Length'], [0, 4, 5, 7, 8], labels=["extra small", "small", "medium", "large"])

# in to 10 groups of equal width across range:
iris['SepalLengthGroup'] = pd.cut(iris['Sepal.Length'], 10, include_lowest=True)

# in to 10 groups of (roughly) equal frequency, note: pd.qcut
dec = pd.Series(range(0, 11)) / 10
iris['PedalSLLengthGroup'] = pd.qcut(iris['Sepal.Length'], q=dec)

# Regrouping, or combining existing groups in to one
animals = pd.Series(("cat", "dog", "flatworm", "kiwi", "sparrow", "fruitfly", "swordfish", "pike", "crocodile"), dtype='category')
zoo = pd.DataFrame({
    'animalID': range(50),
    'spec': np.random.choice(animals, 50),
    'awesomeness': np.random.randn(50)
})
zoo.head()

# To classify these animals as "mammal","bird","fish","reptile","insect", you have to create pairs
# of "old group" - "new group" one way or another.
mammals = {'cat': 'mammal', 'dog': 'mammal'}
zoo['class'] = zoo['spec'].apply(lambda x: mammals.get(x, x))
zoo.head()
zoo.describe()

# Or create a mapping of values, for example like this
# (alvls<-levels(zoo$spec))
# agroup<-c("mammal","reptile","mammal","insect","insect","bird","fish","bird","fish")
# give the old groups as 'names' attribute to the new (that is, create a named vector)
# names(agroup)<-alvls
# agroup
# now you can easily pick the group by name
# zoo$animgroup<-agroup[zoo$spec]

# Or use any of the convenience functions created in to different packages, such as 'recode' in package 'car'

# Working with time stamps and strings in general

weather = pd.read_csv("../datasets/weather-kumpula.csv")

# time stamp is not numeric, so it becomes a factor by default:
weather['ts'].dtype

# Using str:
weather['tssplit'] = weather['ts'].str.split("-")

weather['year'] = weather['tssplit'].str[0]
weather['month'] = weather['tssplit'].str[1]
weather['day'] = weather['tssplit'].str[2]

weather['year'] = weather['ts'].str[:4]
weather['month'] = weather['ts'].str[5:7]
weather['day'] = weather['ts'].str[8:10]

weather['date'] = pd.to_datetime(weather['year'] + '/' + weather['month'] + '/' + weather['day'])

# Load csv with parse_dates argument to get DateTimeIndex
weather = pd.read_csv('../datasets/weather-kumpula.csv', parse_dates=True, index_col=0)
# Now we can use masking

weather[weather.index > "2014-12-01"]
# or slicing
weather[pd.datetime(2014, 6, 25):pd.datetime(2014, 6, 30)]

# And PLEASE whenever you have the say, use the ISO 8601 standard...
