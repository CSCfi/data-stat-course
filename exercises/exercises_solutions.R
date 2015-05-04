#Lecture 1:
rain<-read.csv("rainfall_summer_2014_simple.csv")
#check what you got:
head(rain)
#days appear to be in order, so to draw the barplots...
barplot(rain$rainfall)


#Lecture 2:
#This part was in the lecture notes:
API_BASE_URL<-"http://example.org/api/"

response<-getURL(apiurl)
response<-fromJSON(response)
min_round<-response[["/api/round/<round>"]]$param_min
max_round<-response[["/api/round/<round>"]]$param_max

#and here's the rest of it:
rounds<-min_round:max_round
nrounds<-length(rounds)

response<-fromJSON(getURL(paste0(apiurl,"round/",min_round)))
response$result

results<-matrix(NA,ncol=7,nrow=nrounds)
for(i in 1:nrounds) {  
  result<-fromJSON(getURL(paste0(apiurl,"round/",rounds[i])))$result
  #the following if is needed because some rounds are missing
  if(length(result)==7) results[i,]<-result
}
#we could format this as a data frame but if we are only interested
#in the number frequencies, we can just use it like a vector:
numbers<-as.vector(results)
barplot(table(numbers))

#also, reading from the JSON file:
lotto2000<-fromJSON("lotto-2000.json")
#a cumbersome list... to format this as an array you have to do 
#something like this
nrounds<-length(lotto2000)
numbers<-matrix(NA,ncol=7,nrow=nrounds)
for(i in 1:nrounds) numbers[i,]<-lotto2000[[i]][[2]]
#a more R-like way to do the same:
numbers<-sapply(lotto2000,FUN=function(x) x[[2]])
#and still to a vector etc.
numbers<-as.vector(results)
barplot(table(numbers))


#Lecture 3:
custdata<-read.table("https://github.com/WinVector/zmPDSwR/raw/master/Custdata/custdata.tsv",
                      header=TRUE,sep="\t")
summary(custdata)
#you should immdediatelly see that some incomes are negative
#and that the range of ages is 0 to 146.7
#Is that how it should be?
hist(custdata$income)
#there are some (maybe 1?) very high incomes
hist(custdata$age)
#the ages above 100 are probably some kind of an error?
table(custdata$age)
#also, things to think about: what does it mean that is.employed is missing?
#are the 56 missing values in housing.type, recent.move and num.vehicles the
#same people? how would you find out?

#next, broken slurm data
slurm<-read.table("broken_slurm.csv",sep="|",header=TRUE)
#"line 16 did not have 6 elements"
slurm<-read.table("broken_slurm.csv",sep="|",header=TRUE,fill=TRUE)
summary(slurm)
#Why is there a 6th variable that is completely empty?
#Also, the repeating 20 missing values should raise suspicion
#But it seems there are no missing values in User
summary(slurm$User) 
#something is really fishy! 
#to read the troublesome 16th line
scan("broken_slurm.csv",skip=15,nlines=1,what="character")
#ok, we are starting to see the problem
scan("broken_slurm.csv",skip=15,nlines=2,what="character")
#the lines are broken! We'll get back to fixing this later

#Lecture 4:
custdata2<-read.table("https://github.com/WinVector/zmPDSwR/raw/master/Custdata/custdata2.tsv",
                     header=TRUE,sep="\t")
#recode the TRUE, FALSE and NA values to "employed", "not employed" and "missing"
custdata2$is.employed.fix<-ifelse(custdata2$is.employed,"employed","not employed")
#NA's will stay NA's through that
custdata2$is.employed.fix<-ifelse(is.na(custdata2$is.employed.fix),"missing",custdata2$is.employed.fix)
custdata2$is.employed.fix<-factor(custdata2$is.employed.fix)
#you could also use the fact that booleans become 1 and 0 if you cast them as numeric and start from there!

custdata2$income.group<-cut(custdata2$income,breaks=c(0,10000,50000,100000,250000,1000000),
                            include.lowest=TRUE)
summary(custdata2$income.group)


#Lecture 5:
roo<-read.csv("roots_small.csv")
roowide<-reshape(roo,v.names="length",timevar="meas",idvar="root",direction="wide")
roowide2<-cbind(roowide[1],roowide[3:16]-roowide[2:15])

roolong<-reshape(roowide2,varying=2:15,v.names="growth",timevar="meas",times=2:15,direction="long")
rooagg<-aggregate(growth~meas,roolong,FUN=max,na.rm=TRUE)
plot(rooagg$growth,type="l")

