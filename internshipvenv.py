

import pandas as pd
import numpy as np
import datetime
import pytrends
import os

from pytrends.request_1 import TrendReq


pytrend = TrendReq()
country = pd.read_csv(r"C:\Users\Dell\Desktop\livinglabcountries.csv")

country_list = list(country['living lab countries'])


city = pd.DataFrame()
city = pd.read_csv(r"C:\Users\Dell\Desktop\livinglabcities.csv", encoding = 'latin-1')

city_list= list(city['Field1'])


# In[40]: prepare the sheets for countires in the livinng lab sheet with cities and state codes. also add a timezone to these sheets andun the code

k = r'C:\Users\Dell\Desktop\livinglab.csv'
df1 = pd.read_csv(k, encoding = 'latin-1')
statecodes_list = list(df1['code'])

city_df = pd.Dataframe()



for s in range(len(country_list)):
         py_Df = pytrend.trending_searches(pn=country_list[s])
         count = 0
         for k in statecodes_list:
                 pytrend.build_payload([str(py_Df.iloc[s, 0])], geo=str(k), timeframe='now 1-H')
                 int_city = pytrend.interest_by_city(inc_low_vol=False)
                 for p in range(len(int_city)):
                     if int_city.index[p] in city_list:
                         city_df.loc[count, 'City'] = str(int_city.index[p])
                         city_df.loc[count, 'Value'] = int(int_city[int_city.columns[0]][p])
                         city_df.loc[count, 'Keyword'] = str(df.iloc[i, 0])
                         count = count + 1



# In[42]:


#pytrends.build_payload is a inbuilt pytrends function that is used to build up the functions for a specific
# keyword. if the keyword is india, it is going to provide all the functions necessary to analyze the data
# for several parameters such as intrest over time, concerning the keyword being india.





