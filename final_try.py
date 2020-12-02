#!/usr/bin/env python
# coding: utf-8

# In[39]:


import pandas as pd
import numpy as np
import datetime

import pytrends
from pytrends.request import TrendReq

pytrend = TrendReq(timeout=(5),backoff_factor=60)

from pymongo import MongoClient 

client = MongoClient() 

client = MongoClient("localhost", 27017)

temp_database = client.Google_trends


# In[40]:


df = pytrend.trending_searches(pn='india')
print(df)


# In[41]:


state_list = ['IN-DL','IN-TG','IN-TN','IN-MH','IN-WB','IN-KA']
city_list = ['New Delhi','Hyderabad','Chennai','Mumbai','Kolkata','Bengaluru']
state_name = ['Delhi','Telangana','Tamilnadu','Maharashtra','West Bengal','Karnataka']


# In[42]:


city_df = pd.DataFrame()
count = 0
for i in range(len(df)):
    print(df.iloc[i,0])
    for k in state_list:
        pytrend.build_payload([str(df.iloc[i,0])],geo=str(k),timeframe='now 1-H')
        int_city = pytrend.interest_by_city(inc_low_vol=False)
        for p in range(len(int_city)):
            if int_city.index[p] in city_list:
                city_df.loc[count,'City'] = str(int_city.index[p])
                city_df.loc[count,'Value'] = int(int_city[int_city.columns[0]][p])
                city_df.loc[count,'Keyword'] = str(df.iloc[i,0])
                count = count+1


# In[37]:


for i in range(len(city_list)):
    sorted_df = city_df[city_df['City']==str(city_list[i])].sort_values(by='Value',ascending=False)['Keyword'].reset_index()
    keyword_sorted_list = list(sorted_df['Keyword'])
    rec={
    "City": str(city_list[i]).lower(),
    "State":str(state_name[i]).lower(),
    "date": str(datetime.datetime.now()).split('.')[0],
    "Keywords": keyword_sorted_list,  
    }
    temp_database.India.insert_one(rec) #storing the data onto MongoDB


# In[ ]:




