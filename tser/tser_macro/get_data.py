import pandas as pd, datetime
from pandas_datareader import data
start=datetime.datetime(1950, 1, 1)
end=datetime.datetime(2017, 1, 1)
# Personal Consumption Expenditures - DPCERD3Q086SBEA
# Federal government total expenditures - W019RCQ027SBEA
# State local government total expenditures -  W079RCQ027SBEA
# Real Gross Private Domestic Investment - GPDIC1
# Net Exports of Goods and Services - NETEXP
# Gross Domestic Product - GDP
# Total Credit to Private Non-Financial Sector - CRDQUSAPABIS
# Real Estate Loans, All Commercial Banks - REALLN
df = data.DataReader(['DPCERD3Q086SBEA','W019RCQ027SBEA','W079RCQ027SBEA','GPDIC1','NETEXP','GDP','CRDQUSAPABIS','REALLN'], 'fred', start, end)
df.columns = ['consump','gov1exp','gov2exp', 'invest','netexp','gdp','nonfinloan','constructloan']
df.to_csv('data.csv')