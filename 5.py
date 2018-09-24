# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 23:46:51 2018

@author: pec12003
"""
#Data analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_pickle('df_4.pkl')

#sns.distplot(df.pledged)
#sns.distplot(df.pledged[df.pledged<10000])
#sns.distplot(df.pledged[(df.pledged>10000) & (df.pledged<100000)])
#sns.distplot(df.pledged[(df.pledged>100000) & (df.pledged<1000000)])
#sns.distplot(df.pledged[df.pledged>1000000]) #outlier spotted

df = df[df.pledged != df.pledged.max()]
df = df[df.state != 'suspended']
#state to bool
df_1 = df.state.str.get_dummies()
df_1.drop(columns=['failed'],inplace =True)
df = pd.concat([df,df_1],axis=1)
df.drop(columns=['state','disable_communication'],inplace =True)


#numerical_feat =['goal','pledged','num_sents','num_words','num_all_caps',
#                 'percent_all_caps','num_exclms','percent_exclms','num_buzz_words',
#                 'percent_buzz_words','avg_words_per_sent','num_paragraphs',
#                 'num_images','num_videos','num_gifs','num_hyperlinks','num_bolded',
#                 'percent_bolded','duration','time_to_goal']

corrmat = df.corr()
f, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(corrmat, vmax=.8, square=True)

f, ax = plt.subplots(figsize=(10, 5))
ax = sns.boxplot(x='category', y="pledged", data=df)
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)

sns.boxplot(x='successful', y="pledged", data=df)

sns.boxplot(x='disable_communication', y="pledged", data=df)

# Seperate campaigns into successful ones and failed ones
succ_camp = df[df.successful == 1]
fail_camp = df[df.successful == 0]

f, ax = plt.subplots()
ax = sns.kdeplot(succ_camp.percent_bolded.values,shade=True,label ='successful')
ax = sns.kdeplot(fail_camp.percent_bolded.values,shade=True,label ='failed')
ax.set(xlabel = 'percent_bolded',ylabel = 'PDF')

df_2 = df.category.str.get_dummies()
category_count = df_2.sum()

for col in df_2.columns:
    df_2[col] = (df.successful) & (df_2[col])

category_succ_count = df_2.sum()

df_3 = pd.concat([category_count,category_succ_count],axis=1)  
df_3[2] = df_3[1]/df_3[0]

f, ax = plt.subplots(figsize=(10, 5))
plt.xticks(rotation='vertical')
ax = plt.bar(np.array(df_3.index),df_3[2].values)

df.drop(columns=['avg_words_per_sent','category','num_videos','num_gifs','duration'],inplace=True)
df = pd.concat([df,df_2],axis=1)

df.to_pickle('df_5.pkl')
