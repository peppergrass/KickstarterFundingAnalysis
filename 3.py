# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 10:44:40 2018

@author: pec12003
"""
#Data preparation 1(drop, reform, impute)
import pandas as pd

df = pd.read_pickle("df_2.pkl")
df_3 = df.drop(columns=['blurb','name','urls','normalized_text'])

for i in df_3.index:
    df_3.category[i] = eval(df_3.category[i])['name']
    print(i)
      
df_3 = df_3[df_3.state != 'live'] #remove live caimpaigns


# NaN because campaign is desribed using images or videos
df_3.fillna(0,inplace=True)
#df_3.isnull().sum()

df_3.to_pickle('df_3.pkl') 