import pandas as pd
import numpy as np
nk = pd.read_csv("../datasets/NordklimData.csv", index_col=0)
nks = pd.read_csv("../datasets/NordklimStationCatalogue.csv")

# Subsetting
nksub = nk[nk['CountryCode'] == 'FIN']
nksub = nk.query('CountryCode == "FIN"')
nksub = nk[nk.isin({'CountryCode': ['FIN']}).any(1)]

climate_elements = (101, 111, 112, 113, 121, 122, 123)
nksub = nk[(nk['CountryCode'] == 'FIN') & nk['ClimateElement'].isin(climate_elements)]
nksub = nk.query('CountryCode == "FIN" and ClimateElement in (101,111,112,113,121,122,123)')
nksub = nk[(nk['FirstYear'] == 1900)].loc[:, 'May':'August']  # only summer of 1900

nksnames = nks.loc[:, ('Nordklim.number', 'Station.name')]
nknamed = pd.merge(nk, nksnames, left_on='NordklimNumber', right_on='Nordklim.number')
nk.shape
nknamed.shape

# oops, some Nordklim.numbers don't come with a name apparently, or are completely missing from station catalogue

nknamed = pd.merge(nk, nksnames, left_on='NordklimNumber', right_on='Nordklim.number', how='left')
nk.shape
nknamed.shape

id_vars = ['NordklimNumber', 'CountryCode', 'ClimateElement', 'FirstYear']
nk_rs = pd.melt(nk, id_vars=id_vars, var_name="Month", value_name="value")
months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

nk_rs.replace(to_replace={"Month": months}, inplace=True)

# Aggregation by columns
nk_rs[nk_rs["ClimateElement"] == 101].groupby(by=["CountryCode", "Month"]).agg({'FirstYear': 'first', 'value': np.mean})

nk_rs_pivoted = nk_rs.pivot_table(values="value", index=["NordklimNumber", "Month"],  columns=["ClimateElement"], aggfunc=np.mean)

# Other tools to work with MultiIndex objects: stack & unstack


cols = {
    101: "tempmean", 111: "maxtempmean", 112: "maxtemphi", 113: "temphiday",
    121: "mintempmean", 122: "mintemplow", 123: "temploday", 401: "pressmean",
    601: "precipsum", 602: "precipdmax", 701: "snowcover", 801: "cloudmean"
}

nk_rs_pivoted = nk_rs_pivoted.rename(columns=cols)


for NN in nk["NordklimNumber"].unique():
    nk_rs_pivoted.ix[(NN, ), :]["tempmean"].plot()
