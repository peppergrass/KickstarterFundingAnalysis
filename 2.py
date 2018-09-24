# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:19:53 2018

@author: pec12003
"""

# Clean the scraped data
#Not working campaignDescription ugcContent ng-binding, modal ng-scope top am-slide-right, campaignModal
#Need to try campaignModal-mobile ng-isolate-scope

import pandas as pd
import nltk
nltk.download('punkt')
from bs4 import BeautifulSoup
import numpy as np
import re

scraped_all = pd.read_pickle('scraped_all.pkl')
df = pd.read_csv('df_0.csv')

def parse(scraped_piece): #parse HTML text
    return BeautifulSoup(scraped_piece.text, 'lxml')
def clean_up(messy_text):      
    # Remove line breaks, whitespaces
    clean_text = ' '.join(messy_text.split()).strip() 
    # Remove the HTML5 warning for videos
    return clean_text.replace(
        "You'll need an HTML5 capable browser to see this content. " + \
        "Play Replay with sound Play with sound 00:00 00:00",'')    
def get_campaign(soup):
    #Extract campaign
    try:
        section1 = soup.find('div',
            class_='full-description js-full-description responsive-media formatted-lists').get_text(' ')
    except AttributeError:
        section1 = 'section_not_found'
#    try:
#        section2 = soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').get_text(' ')
#    except AttributeError:
#        section2 = 'section_not_found'        
    return {'campaign': clean_up(section1)}
def normalize(text):
    # Tag email addresses with regex
    normalized = re.sub(
        r'\b[\w\-.]+?@\w+?\.\w{2,4}\b',
        'emailaddr',text) 
    # Tag hyperlinks with regex
    normalized = re.sub(
        r'(http[s]?\S+)|(\w+\.[A-Za-z]{2,4}\S*)',
        'httpaddr',normalized) 
    # Tag money amounts with regex
    normalized = re.sub(r'\$\d+(\.\d+)?', 'dollramt', normalized)
    # Tag percentages with regex
    normalized = re.sub(r'\d+(\.\d+)?\%', 'percntg', normalized)
    # Tag phone numbers with regex
    normalized = re.sub(
        r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        'phonenumbr',normalized)
    # Tag remaining numbers with regex
    return re.sub(r'\d+(\.\d+)?', 'numbr', normalized)
def get_sentences(text):
    # Tokenize the text into sentences
    return nltk.sent_tokenize(text)
def remove_punc(text):
    # Remove punctuation with regex
    return re.sub(r'[^\w\d\s]|\_', ' ', text)
def get_words(text):
    # Remove punctuation and then tokenize the text into words
    return [word for word in nltk.word_tokenize(text)]
def identify_allcaps(text):
    # Identify all-caps words with regex
    return re.findall(r'\b[A-Z]{2,}', text)
def count_exclamations(text):
    # Count the number of exclamation marks in the text
    return text.count('!')
def count_buzz_words(text):
    # Define a set of buzz words
    buzz_words = frozenset(
        ['revolutionary', 'breakthrough', 'beautiful', 'magical', 
        'gorgeous', 'amazing', 'incredible', 'awesome','data','intelligence'])
    return sum(1 for word in get_words(text) if word in buzz_words)
def compute_avg_words(text):
    # Compute the average number of words in each sentence
    return pd.Series(
        [len(get_words(sentence)) for sentence in get_sentences(text)]
    ).mean()
def count_paragraphs(soup, section):    
    # Count the number of paragraphs
    if section == 'campaign':
        return len(soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('p')) 
#        + len(soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('p'))
#        )
def count_images(soup, section):    
    # Use tree parsing to identify all image tags 
    if section == 'campaign':
        return len(soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('img')) 
#            +len(soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('img'))
#        )
def count_videos(soup, section):    
    # Count all videos
    youtube_count = 0
    non_youtube_count = 0
    if section == 'campaign':
        non_youtube_count = len(soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('video-player')) 
#            +len(soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('video-player'))
#        )
        youtube = soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('iframe')
#        +
#        soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('iframe'))
    for iframe in youtube:
        try:
            if 'youtube' in iframe.get('src'):
                youtube_count += 1
        except TypeError:
            pass
    return youtube_count+non_youtube_count
def count_gifs(soup, section):    
    gif_count = 0
    # Use tree parsing to select all image tags depending on the section
    # requested
    if section == 'campaign':
        images = soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('img')
#            +
#        soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('img'))   
    for image in images:
        # Catch any iframes that fail to include an image source link
        try: 
            if 'gif' in image.get('data-src'):
                gif_count += 1
        except TypeError:
            pass
    return gif_count
def count_hyperlinks(soup, section):    
    # Use tree parsing to compute number of hyperlink 
    if section == 'campaign':
        return  len(soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('a')) 
#            +len(soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('a'))
#        )
def count_bolded(soup, section):    
    # Use tree parsing to compute number of bolded text 
    if section == 'campaign':
        return  len(soup.find('div',
            class_='full-description js-full-description responsive-media ' + \
                'formatted-lists').find_all('b')) 
#        +len(soup.find('div',
#            class_='mb3 mb10-sm mb3 js-risks').find_all('b'))
#        )
def preprocess_text(text):    
    # Access stop word dictionary
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # Initialize the Porter stemmer
    porter = nltk.PorterStemmer()    
    # Remove punctuation and lowercase each word
    text = remove_punc(text).lower()    
    # Remove stop words and stem each word
    return ' '.join(porter.stem(term )
        for term in text.split()
        if term not in set(stop_words))


def extract_features(soup, campaign, section):
    # Compute the number of words in the requested section
    num_words = len(get_words(campaign[section]))    
    # If the section contains no words, assign NaN to 'num_words' to avoid
    # potential division by zero
    if num_words == 0:
        num_words = np.nan
    if campaign[section] == 'section_not_found':
        return([np.nan] * 17)
    else:
        return (
            len(get_sentences(campaign[section])),
            num_words,
            len(identify_allcaps(campaign[section])),
            len(identify_allcaps(campaign[section])) / num_words,
            count_exclamations(campaign[section]),
            count_exclamations(campaign[section]) / num_words,
            count_buzz_words(campaign[section]),
            count_buzz_words(campaign[section]) / num_words,
            compute_avg_words(campaign[section]),
            count_paragraphs(soup, section),
            count_images(soup, section),
            count_videos(soup, section),
            count_gifs(soup, section),
            count_hyperlinks(soup, section),
            count_bolded(soup, section),
            count_bolded(soup, section) / num_words,
            campaign[section])

# Initialize empty DataFrames of features for each section
features = ['num_sents', 'num_words', 'num_all_caps', 'percent_all_caps',
            'num_exclms', 'percent_exclms', 'num_apple_words',
            'percent_apple_words', 'avg_words_per_sent', 'num_paragraphs',
            'num_images', 'num_videos', 'num_gifs',
            'num_hyperlinks', 'num_bolded', 'percent_bolded',
            'normalized_text']
section_df = pd.DataFrame(columns=features)

for index, row in scraped_all.iterrows():
    # Parse scraped HTML
    soup = parse(row[0])
    # Extract and normalize campaign sections
    campaign = get_campaign(soup)
    campaign['campaign'] = normalize(campaign['campaign'])
    # Extract meta features for each section
    section_df.loc[index] = extract_features(soup, campaign, 'campaign')           

df_2 =  pd.merge(df,section_df, left_index=True, right_index=True)         
df_2.to_pickle('df_2.pkl')
                