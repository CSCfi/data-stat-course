height<-sample(13:300,900,replace=TRUE)
diam<-round(height/7*(1+rnorm(900,sd=0.2)))
height<-c(height,rep(-9999,90),rep(NA,5))
height<-c(height,rep("E",5))
diam<-c(diam,rep(NA,100))
height[1]<-540

treeID<-as.character(sample(100001:300099,1000))
plotID<-substr(x = treeID,start=1,stop=4)
treeID<-substr(x=treeID,start=5,stop=6)
species<-sample(1:2,1000,replace=TRUE,prob=c(8,2))
species[2]<-1.2

faketrees<-data.frame(plotID=plotID,treeID=treeID,species=species,height=height,diam=diam)
faketrees<-faketrees[sample(dim(faketrees)[1]),]
write.csv(faketrees,file="faketrees.csv",quote=FALSE,row.names=FALSE,na="")
rm(height,diam,treeID,plotID,species,faketrees)
