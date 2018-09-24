# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 22:45:03 2018

@author: pec12003
"""

#Pre-processing

import pandas as pd


df0 = pd.read_csv('Kickstarter.csv')
df1 = pd.read_csv('Kickstarter001.csv')
df2 = pd.read_csv('Kickstarter002.csv')
df3 = pd.read_csv('Kickstarter003.csv')
df4 = pd.read_csv('Kickstarter004.csv')
df5 = pd.read_csv('Kickstarter005.csv')
df6 = pd.read_csv('Kickstarter006.csv')
df7 = pd.read_csv('Kickstarter007.csv')
df8 = pd.read_csv('Kickstarter008.csv')
df9 = pd.read_csv('Kickstarter009.csv')

df = pd.concat([df0,df1,df2,df3,df4,df5,df6,df7,df8,df9])

df_0 = df.drop(['creator','country','converted_pledged_amount',
                'currency_symbol','fx_rate','currency_trailing_code',
                'current_currency','id','photo','profile',
                'source_url','static_usd_rate','slug','location',
                'usd_type','friends','is_backing','is_starred',
                'permissions','usd_pledged','usd_type'],axis=1)

df_0 = df_0[df_0.currency == 'USD']
df_0.drop(['currency'],axis=1,inplace=True)

df_0.to_csv('df_0.csv',index=False)