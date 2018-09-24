# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:04:10 2018

@author: pec12003
"""

#Scrape more text data from URL

import pandas as pd
import requests
import time
import random
#from bs4 import BeautifulSoup

df_0 = pd.read_csv('df_0.csv')

scraped_all = pd.DataFrame(columns=['scraped_info'])
request_count = 0

for index, row in df_0.loc[6759:].iterrows():
    scraped_piece  = requests.get(eval(row.urls)['web']['project'], timeout = 200)
  
    if index//100==0: time.sleep(random.uniform(2,4))
    
    print('Request: {}'.format(request_count))
    request_count += 1
    scraped_all.loc[index,'scraped_info'] = scraped_piece
    
scraped_all.to_pickle('scraped_all.pkl')