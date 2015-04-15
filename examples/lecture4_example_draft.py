# Lecture 4: "more wrangling"

import pandas as pd
import numpy as np

# Just a reminder, adding new variables to data frames is easy, for example:
iris = pd.read_csv('https://raw.github.com/pydata/pandas/master/pandas/tests/data/iris.csv')
iris.columns

iris['SepalArea'] = iris['SepalLength'] * iris['SepalWidth']
iris.columns
#Note that this works (only) because row order is fixed.
#Pandas data frame is smarter in this sense

# Replacing whole columns works the same way.
# To remove a single column DataFrame objects have drop method, which returns a *new*
# DataFrame with the chosen column dropped
iris2 = iris.drop('SepalArea', 1)
iris2.columns
iris.columns

# The column may be removed from a DataFrame object with del statement
del iris['SepalArea']
iris.columns

# loc:  label based indexing
# iloc: integer based indexing:
# XXX: Remember, indexing starts from zero, ":" selects whole axis
iris.head().iloc[:, :5] #pick just the first 5 columns

# By negative column index:
iris.head().iloc[:, :-1] #pick everything but the last column

# By column name:
iris.head().loc[:, ["SepalLength","SepalWidth","PetalLength","PetalWidth","Species"]]

# Unfortunately, negative column names don't work, and there are no inverse matching.
cols = iris.columns.tolist()  # list of column names
cols.remove('SepalArea')
iris.head().loc[:, cols]

# Binning, or making a continuous variable in to a discrete one
# Let's make a histogram of the sepal lengths
plt.hist(iris$Sepal.Length)
plt.show()

print "Values for SepalLength range from %s to %s" % (iris['SepalLength'].min(), iris['SepalLength'].max())
iris['SepalLengthGroup'] = pd.cut(iris['SepalLength'], [0,4,5,7,8], labels=["extra small", "small","medium","large"])

#in to 10 groups of equal width across range:
iris['PedalLengthGroup'] = pd.cut(iris['SepalLength'], 10, include_lowest=True)

#in to 10 groups of (roughly) equal frequency, note: pd.qcut
dec = pd.Series(range(0, 11))/10
iris['PedalLengthGroup'] = pd.qcut(iris['SepalLength'], q=dec)

# Regrouping, or combining existing groups in to one
animals = pd.Series(("cat","dog","flatworm","kiwi","sparrow","fruitfly","swordfish","pike","crocodile"), dtype='category')
zoo = pd.DataFrame({
    'animalID': range(50),
    'spec': np.random.choice(animals, 50),
    'awesomeness': np.random.randn(50)
})
zoo.head()

# To classify these animals as "mammal","bird","fish","reptile","insect", you have to create pairs
# of "old group" - "new group" one way or another.
mammals = {'cat': 'mammal', 'dog': 'mammal'}
zoo['class'] = zoo['spec'].apply(lambda x: animalToClass.get(x, x))
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

# weather<-read.csv("https://raw.githubusercontent.com/CSC-IT-Center-for-Science/data-stat-course/master/datasets/weather-kumpula.csv")

# time stamp is not numeric, so it becomes a factor by default:
# class(weather$ts)
# could have read the data with 'as.is=TRUE' argument, or can change the factor in to corresponding strings by
# weather$ts<-as.character(weather$ts)
# NB! be very careful when trying to change factors in to numeric. See the warning on factor help page

# Let's take the year, month and day apart and put them in the data frame as separate columns. Note that
# this might not always be sensible, and you might want to change it to a date-time object instead. That
# is covered soon. Here, dates serve as an example of a string.

# Using strsplit:
# ts.split<-strsplit(weather$ts,split="-")
# The result is a list as long as long as the original character vector, whose elements are character vectors
# containing the split parts.
# class(ts.split)
# ts.split[[1]]
# In this case each element of the list of the same length so it's possible to do:
# ts.split<-simplify2array(ts.split)
# dim(ts.split) #year, month, day as rows
# weather$year<-ts.split[1,]
# weather$month<-ts.split[2,]
# weaher$day<-ts.split[3,]
# Now they can be changed to numeric or factor as needed

# Using substr:
# Since the dates are nice here, each field taking the same number of characters, it is also possible to do:
# weather$year<-substr(weather$ts,start=1,stop=4)
# weather$month<-substr(weather$ts,start=6,stop=7)
# weather$day<-substr(weather$ts,start=9,stop=10)

# The other way around: from numeric to character
# dates<-weather[c("year","month","day")]
# for(n in names(dates)) dates[[n]]<-as.numeric(dates[[n]])
# Basically, this is easy using:
# with(dates,head(paste(year,month,day,sep="-")))
# paste will stick the parts together, separated by whatever you give as 'sep'. If the parts are not
# character to  begin with, they will be coerced via 'as.character'

# Note that this leaves out the filling 0's. There are ways to get them too (see 'format' for example) 
# but to deal with dates specifically it is best to use the date-time classes

# names(weather)
# weather$datetime<-strptime(weather$ts,format="%F")
# summary(weather)
# weather$date<-as.Date(weather$datetime)
# summary(weather)
# Now getting these back as strings is easy:
# head(as.character(weather$datetime)) 
# See also format.Date
# And PLEASE whenever you have the say, use the ISO 8601 standard...
