#Lecture 5: even more wrangling
#Lecture 4 focused on manipulations that deal with single columns at a time. Now let's do things with whole data frmaes

nk<-read.csv("../datasets/NordklimData.csv")
nks<-read.csv("../datasets/NordklimStationCatalogue.csv")


#Subsetting
nksub<-subset(nk,CountryCode=="FIN") #only Finland
nksub<-subset(nk,CountryCode=="FIN"&ClimateElement%in%c(101,111:113,121:123)) #temperature measurements in Finland only
nksub<-subset(nk,FirstYear==1900,select=May:August) #only summer of 1900
#subset is a human friendly way of referring to rows and columns intended for interactive use, it is recommended
#to use [ , ] in code that gets used multiple times


#Combining two data frames
#To add a column of station names to the nk data from the nks data:
nksnames<-subset(nks,select=c(Nordklim.number,Station.name))
nknamed<-merge(nk,nksnames,by.x="NordklimNumber",by.y="Nordklim.number")
dim(nk)
dim(nknamed)
#oops, some Nordklim.numbers don't come with a name apparently, or are completely missing from station catalogue
nknamed<-merge(nk,nksnames,by.x="NordklimNumber",by.y="Nordklim.number",all=TRUE) 
#ALL=TRUE means rows with no match are included, filled with NA where necessary
dim(nk)
dim(nknamed)
#and there seem to be some extra stations in the catalogue as well!
#Idea for an exercise: learn the nature of this mismatch!

#Also: cbind and rbind for simply sticking more columns or rows to the data frame
#For cbind the row order must be matched manually beforehand
#For rbind column order is irrelevant as long as the column names match


#Reshaping between long and wide:
#Usually it is preferred to have the data in a form where:
#-each column is a variable
#-each row is an observation
#(Long format)
#Nordklim now has many observations per row, and also many variables per column. 
#We can reshape it (going frist from wide to long):

nk.rs<-reshape(nk,
               varying=match("January",names(nk)):match("December",names(nk)),
               v.names="value",
               timevar="month",times=1:12,
               direction="long")
#Note that reshape generated an extra id column which we don't need
#And while we're at it, throw away the original index as well
nk.rs<-subset(nk.rs,select=-c(id,X))
#Now each row is an observation, but "value" still contains many variables

nk.rs<-subset(nk.rs,CountryCode=="FIN") #To make the next call a bit faster

nk.rs2<-reshape(nk.rs,
                v.names="value",
                timevar="ClimateElement",
                idvar=c("NordklimNumber","FirstYear","month"),
                direction="wide")

#Ok, it seems there are multiple records of the same variable for some places, let's find out:
nk.test<-subset(nk.rs,select=c(NordklimNumber,FirstYear,month,ClimateElement))
#No row should be repeated, right? But:
sum(duplicated(nk.test))
#There are 24 rows in this subset that are copies of an earlier one

#Another idea for an exercise: see if it's possible to figure out which record is correct

#Oh well, here we just used only the first. And now we have the data frame as we wanted:
head(nk.rs2)
#As a final touch, we could replace the column names with sensible ones:
names(nk.rs2)[5:16]<-c("tempmean",
                       "maxtempmean",
                       "maxtemphi",
                       "temphiday",
                       "mintempmean",
                       "mintemplow",
                       "temploday",
                       "pressmean",
                       "precipsum",
                       "precipdmax",
                       "snowcover",
                       "cloudmean")
#Now for example a summary makes sense:
summary(nk.rs2)
#And here we see why -9999 is a lousy way to mark a missing value
#Luckily it is easy to fix
nk.rs2[nk.rs2==-9999]<-NA
#And life later on is much easier if we represent dates as dates:
nk.rs2$date<-with(nk.rs2,as.Date(paste0(FirstYear,"-",month,"-",1)))
summary(nk.rs2)

#(We also see an example of summary quickly showing problems: what is the day number 80 within a month?)


#We can now start making some kind of analyses. Finally!

#Aggregation: calculate a groupwise summary value, such as:
#Average monthly temperatures (over a year) at different stations:

tmp<-aggregate(tempmean~month+NordklimNumber,data=nk.rs2,FUN=mean)
#(save this for the next lecture:) 
write.csv(tmp,file="monthtemps.csv")
head(tmp)
plot(tempmean~month,data=tmp)

#With simple R plots, in order to draw a curve for each station, you have to 
#draw one curve at a time on top of each other.

for(NN in unique(tmp$NordklimNumber))
  lines(tempmean~month,data=tmp,subset=NordklimNumber==NN)

#Of course you would like to have the different stations as different colors
#but this graph can't be made readable anyway, it is just for demonstration

#Note that there is a more R-like way to do the previous for-loop, either
#using the function 'by' or functions 'split' and 'lapply'

#Also note that for the previous line drawing to work the rows needed to be in order
#according to the month number, otherwise the result is a mess. Aggregate automatically
#orders the result, but when needed it can be done explicitly.
#First, a random permutation:
head(tmp)
tmp<-tmp[sample(nrow(tmp)),]
head(tmp)
tmp<-tmp[order(tmp$NordklimNumber),]
head(tmp)
tmp<-tmp[order(tmp$month,tmp$NordklimNumber),]
head(tmp) #order by the first argument, splitting ties by the second etc
