# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:12:54 2018

@author: pec12003
"""

# Predictive modeling

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error



df = pd.read_pickle('df_5.pkl')
y_features = ['successful','pledged','time_to_goal']
x_features = list(set(np.array(df.columns))-set(y_features))
X = df[x_features]
y0 = df[y_features[0]]


#X_train, X_test, y_train, y_test = train_test_split(X,y0,test_size=0.2)
#random_forest = RandomForestClassifier()
#random_forest.fit(X_train,y_train)
#score = random_forest.score(X_test,y_test)
#
#xg_boost = xgb.XGBClassifier()
#xg_boost.fit(X_train,y_train)
#score_1 = accuracy_score(y_test, xg_boost.predict(X_test))

#Money pledged
df_funded = df[df.successful == 1]
X = df_funded[x_features]
y = df_funded[y_features[2]]
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
xg_boost = xgb.XGBRegressor()
xg_boost.fit(X_train,y_train)
y_predict = xg_boost.predict(X_test)  
score = mean_squared_error(y_test, y_predict)

plt.plot(range(1,4045),y_test.values-y_predict)
#plt.plot(range(1,4045),)