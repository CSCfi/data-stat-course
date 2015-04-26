#Lecture 6: Graphs. Fitting simple models

#Quick review of typical graph types

#Simple frequencies by group: barplot
tmp<-data.frame(group=factor(sample(LETTERS[1:5],100,replace=TRUE,prob = c(1,1,2,3,4))))
barplot(xtabs(~group,tmp))

#Cross tabulations of frequencies by two groupings:
#stacked or grouped barplots
tmp$anothergroup<-factor(sample(letters[23:26],100,replace=TRUE))
barplot(xtabs(~anothergroup+group,tmp),beside=TRUE,legend=TRUE)
#possibly as proportions:
barplot(prop.table(xtabs(~anothergroup+group,tmp),2),legend=TRUE)
#proportions maybe as pie charts as well. maybe.

#Continuous variable by group: 
tmp$xvar<-with(tmp,rnorm(100,sd=(1:4)[anothergroup]))
#boxplots, if you are interested in mean differences, analysis of variance style
boxplot(xvar~group,tmp)
boxplot(xvar~group+anothergroup,tmp)
#density function estimates, if you are interested in the shape of the distributions
plot(density(subset(tmp,anothergroup=="w")$xvar))
#to draw multiple density functions on the same graph, you have to add the later ones
#using 'lines' one by one, but at least the object is suitable for that without
#further tweaks:
lines(density(subset(tmp,anothergroup=="x")$xvar),col="red")
lines(density(subset(tmp,anothergroup=="y")$xvar),col="blue")
#and here we start seeing that some things are not too simple to do

#Time series, growth curves; continuous variable by time (or time-like variable)
#(Note that there is an actual time series object available.)
#Line graphs: this was actually already seen in the last lecture, just making a point here:
tmp2<-data.frame(y=runif(15),t=1:15)
plot(y~t,tmp2,type="l") #fine
tmp2<-data.frame(y=runif(15),t=sample(15))
plot(y~t,tmp2,type="l") #NOT fine!
#The fact that you have to manually order the values is annoying and/or oldfashioned

#Continuous variable by another continuous variable:
tmp$yvar<-1+2*tmp$xvar+rnorm(100,sd=2)
#scatterplot
plot(yvar~xvar,tmp)
#coloring & symbols by groups:
plot(yvar~xvar,tmp,col=group,pch=(1:4)[anothergroup])
#or you might want or need to do it group by group:
plot(yvar~xvar,tmp,type="n") #no points are actually plotted, but this is a handy
#way to get suitable axis limits automatically
points(yvar~xvar,tmp,subset=group=="A",col="black",pch=16)
points(yvar~xvar,tmp,subset=group=="B",col="blue",pch=17,cex=3)
#etc


#simple R plots are fine for quick graphing end exploring.
#With anything more complicated ggplot will soon be a far better approach

#library(ggplot2)

mt<-read.csv("monthtemps.csv") #the aggregate data from last lecture
mt<-mt[sample(nrow(mt)),] #make sure it's unordered
mt$NNf<-factor(mt$NordklimNumber)

#scatterplot:
ggplot(mt)+geom_point(aes(x = month,y=tempmean))

#scatterplot with groups shown
ggplot(mt)+geom_point(aes(x = month,y=tempmean,col=NNf))
#note that here "col=factor" is not literal as it is with R plots!

ggplot(mt)+geom_line(aes(x = month,y=tempmean,col=factor(NordklimNumber)))
#"make lines of this variable by that, groups differentiated by color" 
#(this shows the power of the 'grammar of graphics' approach!)

#each curve in its own plot
ggplot(mt)+geom_line(aes(x=month,y=tempmean))+facet_wrap(~NNf)


#Fitting linear models:
#minimal example: you name the response and a continuous explaining variable, 
#you get the intercept and the coefficient for the explaining variable
lm(yvar~xvar,tmp)
#A bit more:
fit<-lm(yvar~xvar,tmp)
summary(fit) #significance tests for the coefficients, R-squared, F-test
#note the similarity between the scatterplot and lm syntax:
plot(yvar~xvar,tmp)
#adding the fitted line:
abline(fit)

#the same graph with ggplot:
ggplot(tmp,aes(xvar,yvar))+geom_point()+stat_smooth(method="lm")
#separate model for each group:
ggplot(tmp,aes(xvar,yvar))+geom_point()+stat_smooth(method="lm")+facet_wrap(~group)

#a factor instead of a continuous variable as explaining variable:
fit<-lm(yvar~group,tmp)
summary(fit) #t-tests for each level coefficient (H0: same mean as base level group)
anova(fit)       

#main effects of a factor and a continuous variable:
summary(lm(yvar~group+xvar,tmp))
#each group has its own intercept

#all main effects and interactions:
summary(lm(yvar~group*xvar,tmp))
#each group has its own intercept and coefficient
#equal to:
summary(lm(yvar~group+xvar+group:xvar,tmp))
       
#common intercept, different coefficients:
summary(lm(yvar~xvar+group:xvar,tmp))

#more complicated regression models: nls for nonlinear least squares,
#glm for generalized linear models, nlme for linear & nonlinear mixed effects