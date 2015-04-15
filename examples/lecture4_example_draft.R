#Lecture 4: "more wrangling"

#Just a reminder, adding new variables to data frames is easy, for example:
data(iris)
names(iris)
iris$Sepal.Area<-with(iris,Sepal.Length*Sepal.Width)
names(iris)
#Note that this works (only) because row order is fixed.
#Pandas data frame is smarter in this sense

#Replacing whole columns works the same way.
#To remove a single column:
iris$Sepal.Area<-NULL
names(iris)

#all of the following do the same in this case

#by column index:
iris<-iris[1:5] #pick just the first 5 columns

#by negative column index:
iris<-iris[-6] #pick everything but the 6th column

#by column name:
iris<-iris[c("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width","Species")]

#unfortunately, negative column names don't work, have to do this:
iris<-iris[-match(names(iris),"Sepal.Area")] #pick everything that isn't called...
#(gives an error if there isn't one)
#(actually, the function 'subset' would do that too, we'll get back to that later)



#Binning, or making a continuous variable in to a discrete one
hist(iris$Sepal.Length)
range(iris$Sepal.Length)
iris$SLgroup<-cut(iris$Sepal.Length,breaks=c(0,4,5,7,8),labels=c("small","medium","large"))

#in to 10 groups of equal width across range:
intr<-with(iris,seq(min(Sepal.Length),max(Sepal.Length),length.out=11))
iris$SLgroup<-cut(iris$Sepal.Length,breaks=intr,include.lowest=TRUE)

#in to 10 groups of (roughly) equal frequency (in to a numeric, not factor, this time):
dec<-quantile(iris$Sepal.Length,probs = (0:10)/10)
iris$SLgroup<-cut(iris$Sepal.Length,breaks=dec,labels=FALSE,include.lowest=TRUE)


#Regrouping, or combining existing groups in to one
zoo<-data.frame(animalID=1:50,
                spec=factor(sample(c("cat","dog","flatworm","kiwi","sparrow","fruitfly","swordfish","pike","crocodile"),
                                   50,replace=TRUE)),
                awesomeness=rnorm(50))
head(zoo)
#To classify these animals as "mammal","bird","fish","reptile","insect", you have to create pairs
#of "old group" - "new group" one way or another.

#You could go one group at a time (a bit convoluted but simple if you only need to group some and
#leave others as is:
zoo$animgroup<-with(zoo,ifelse(spec%in%c("cat","dog"),"mammal",levels(spec)[spec]))
head(zoo) #NB! animgroup is a character vector
summary(zoo)
zoo$animgroup<-factor(zoo$animgroup)
#rinse repeat

#Or create a mapping of values, for example like this
(alvls<-levels(zoo$spec))
agroup<-c("mammal","reptile","mammal","insect","insect","bird","fish","bird","fish")
#give the old groups as 'names' attribute to the new (that is, create a named vector)
names(agroup)<-alvls
agroup
#now you can easily pick the group by name
zoo$animgroup<-agroup[zoo$spec]

#Or use any of the convenience functions created in to different packages, such as 'recode' in package 'car'

#Working with time stamps and strings in general

weather<-read.csv("https://raw.githubusercontent.com/CSC-IT-Center-for-Science/data-stat-course/master/datasets/weather-kumpula.csv")

#time stamp is not numeric, so it becomes a factor by default:
class(weather$ts)
#could have read the data with 'as.is=TRUE' argument, or can change the factor in to corresponding strings by
weather$ts<-as.character(weather$ts)
#NB! be very careful when trying to change factors in to numeric. See the warning on factor help page

#Let's take the year, month and day apart and put them in the data frame as separate columns. Note that
#this might not always be sensible, and you might want to change it to a date-time object instead. That
#is covered soon. Here, dates serve as an example of a string.

#Using strsplit:
ts.split<-strsplit(weather$ts,split="-")
#The result is a list as long as long as the original character vector, whose elements are character vectors
#containing the split parts.
class(ts.split)
ts.split[[1]]
#In this case each element of the list of the same length so it's possible to do:
ts.split<-simplify2array(ts.split)
dim(ts.split) #year, month, day as rows
weather$year<-ts.split[1,]
weather$month<-ts.split[2,]
weaher$day<-ts.split[3,]
#Now they can be changed to numeric or factor as needed

#Using substr:
#Since the dates are nice here, each field taking the same number of characters, it is also possible to do:
weather$year<-substr(weather$ts,start=1,stop=4)
weather$month<-substr(weather$ts,start=6,stop=7)
weather$day<-substr(weather$ts,start=9,stop=10)

#The other way around: from numeric to character
dates<-weather[c("year","month","day")]
for(n in names(dates)) dates[[n]]<-as.numeric(dates[[n]])
#Basically, this is easy using:
with(dates,head(paste(year,month,day,sep="-")))
#paste will stick the parts together, separated by whatever you give as 'sep'. If the parts are not
#character to  begin with, they will be coerced via 'as.character'

#Note that this leaves out the filling 0's. There are ways to get them too (see 'format' for example) 
#but to deal with dates specifically it is best to use the date-time classes

names(weather)
weather$datetime<-strptime(weather$ts,format="%F")
summary(weather)
weather$date<-as.Date(weather$datetime)
summary(weather)
#Now getting these back as strings is easy:
head(as.character(weather$datetime)) 
#See also format.Date
#And PLEASE whenever you have the say, use the ISO 8601 standard...
