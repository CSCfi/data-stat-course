import pandas as pd
import matplotlib.pyplot as pl

weather = pd.read_csv(
    "../datasets/weather-kumpula.csv",
    header=0,
    index_col=0,
    parse_dates=True)

weather.head()
weather['rmm'].plot()


ax1 = weather.t.plot(style='r-', legend=False, title="Weather 2014 (Kumpula, Helsinki)")
ax2 = weather.rmm.plot(secondary_y=True, style='b.')
ax1.set_ylabel("average temperature per day (celcius)")
ax2.right_ax.set_ylabel("cumulated rainfall per day (mm)")


#Lecture 2:
#This part was in the lecture notes:
API_BASE_URL<-"http://example.org/api/"
response = requests.get(API_BASE_URL).json()
min_round = response['/api/round/<round>']['param_min']
max_round = response['/api/round/<round>']['param_max']
print "min_round: %s max_round: %s" % (min_round, max_round)

results = []
for i in range(min_round, max_round + 1):
    response = requests.get(API_BASE_URL + 'round/%s' % (min_round + i)).json()
    result = response.get('result')
    if result:
        results.extend(result)

numbers = pd.Series(results)
numbers.hist(bins=39, normed=True)

# also, reading from the JSON file:
import json
lotto2000 = json.load(open("../datasets/lotto-2000.json"))
results = []
for l in lotto2000:
    results.extend(l[1])


#Lecture 3:
custdata = pd.read_table("https://github.com/WinVector/zmPDSwR/raw/master/Custdata/custdata.tsv")
custdata.describe(include='all')

#you should immdediatelly see that some incomes are negative
#and that the range of ages is 0 to 146.7
#Is that how it should be?
custdata.income.hist()
#there are some (maybe 1?) very high incomes
custdata.age.hist()
#the ages above 100 are probably some kind of an error?
sorted(custdata.age.unique())
#also, things to think about: what does it mean that is.employed is missing?
#are the 56 missing values in housing.type, recent.move and num.vehicles the
#same people? how would you find out?

#next, broken slurm data
slurm = pd.read_table("../datasets/broken_slurm.csv", sep="|",)
slurm.describe(include='all')

#column Unnamed: 0...
#Why is there a 6th variable that is completely empty?
#Also, the repeating 20 missing values should raise suspicion
#But it seems there are no missing values in User
slurm.User.unique()

#something is really fishy! 
slurm.ix[13:16, ]
#the lines are broken! We'll get back to fixing this later

#Lecture 4:
custdata2<-read.table("https://github.com/WinVector/zmPDSwR/raw/master/Custdata/custdata2.tsv",
                     header=TRUE,sep="\t")
mappings = {True: 'employed', False: 'not employed', np.NaN: 'missing'}
custdata2['is.employed'] = custdata2['is.employed'].map(mappings)

custdata2['income.group'] = pd.cut(custdata2.income, [0,10000,50000,100000,250000,1000000], include_lowest=True)

custdata2['income.group'].describe()


#Lecture 5:
roo<-read.csv("../datasets/roots_small.csv")
roowide = roo.pivot(index='root', columns='meas')


# Because of data alignment, the column names must match
#s1 = roowide.ix[:,:-1]
#s2 = roowide.ix[:,1:]
#s1 = s1.rename(columns= dict([(x, x+1) for x in range(1, 14)]))
#roowide2 = s2 - s1

# a bit cumbersome...

# Column renaming can be avoided with numpy, but data alignment is lost
#roowide2 = DataFrame(np.array(roowide.ix[:,1:]) - np.array(roowide.ix[:,:-1]))
#roowide2.index = roowide.index


roowide2 = pd.np.subtract(roowide.ix[:,1:], roowide.ix[:,:-1])

roolong = roowide2.stack().reset_index()

rooagg = roolong.groupby('meas').max()
rooagg.plot()
