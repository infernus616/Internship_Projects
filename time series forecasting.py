from datetime import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color']='k'

#we are going to carry out a time series analysis for the existing
#dataset assuming that it is a time series distribution.

#we will then forecast this data and fit it with the actual data for analysis

df = pd.read_csv(r"C:\Users\Dell\Desktop\forecasting2.csv")
df = df.fillna(0)
df = df.iloc[:,0:13]

plt.figure(figsize=(80,200))
x=[]
for i in range(0,64):
    x.append(i)


col1 = pd.DataFrame(df, columns=["keyword rank", "hour"])
for i in range(1, len(df.columns)):
         name = df.columns[i]
         col1["keyword rank"] = df.iloc[:,i]
         col1["keyword rank"] = col1["keyword rank"].fillna(0)

         col1["hour"] = pd.Series(range(0,63))
         col1["keyword rank"] = col1["keyword rank"].astype(int)
         col1["hour"] = col1["hour"].fillna(0)
         col1["hour"] = col1["hour"].astype(int)
         from pylab import rcParams
         rcParams['figure.figsize'] = 5,8
         decomposition = sm.tsa.seasonal_decompose(col1["keyword rank"], period=1, model= "additive")
         mod = sm.tsa.statespace.SARIMAX(col1["keyword rank"], order=(1,1,1), seasonal_order =(1,1,0,12), enforce_stationarity=False, enforce_invertibility= False)
         results = mod.fit()
         y =col1["keyword rank"].mean()
         pred = results.get_prediction(start = col1["hour"].iloc[10],dynamic= False)
         pred_ci = pred.conf_int()
         plt.figure(i)
         plt.plot(col1["hour"], col1["keyword rank"])
         pred.predicted_mean.plot(label = "forecast", alpha = 0.7, figsize =(8,8))
         col1["keyword rank"] = col1["keyword rank"].astype('timedelta64[D]')
         plt.title(str(name))
         plt.legend()




plt.show()