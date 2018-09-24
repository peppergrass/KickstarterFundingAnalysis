# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 22:44:52 2018

@author: pec12003
"""
#Data preparation 2

import pandas as pd


df = pd.read_pickle('df_3.pkl')

df_describe = df.describe() #take a look at the data available



df[df.pledged==df.pledged.max()]

df.drop(columns='created_at',inplace=True)
df = df[df.state != 'canceled']
#Successful campaign still get money after
df['duration'] = df['deadline']- df['launched_at']
df['time_to_goal'] = df['state_changed_at']- df['launched_at']  

df.drop(columns=['deadline','launched_at','backers_count','is_starrable',
                 'spotlight','staff_pick','state_changed_at'],inplace=True)
df = df.rename({'num_apple_words':'num_buzz_words',
           'percent_apple_words':'percent_buzz_words'},axis =1)

df.to_pickle('df_4.pkl') 