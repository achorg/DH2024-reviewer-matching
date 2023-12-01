import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 
import time 
import random

reviewers = pd.read_csv('DH2024WashingtonDC_reviewers_2023-11-29_15-19-51.csv')
reviewer_fields = ['personID', 'name','firstname','topics','maxreviews']
reviewer_df = reviewers[reviewer_fields]

#only 147 have a maxreviews, set default of 3
reviewer_df['maxreviews'] = reviewer_df['maxreviews'].fillna(3)

# https://stackoverflow.com/questions/22623798/google-search-with-python-requests-library
headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

pbar = tqdm(total=len(reviewer_df))
def google(row):
    first_name = row['firstname']
    last_name = row['name']
    s = requests.Session()
    q = f'{first_name}+{last_name}+digital+humanities'
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    time.sleep(random.randrange(4, 7))
    return soup.text

def scholar(row):
    first_name = row['firstname']
    last_name = row['name']
    s = requests.Session()
    q = f'{first_name}+{last_name}+digital+humanities'
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C39&q=' + q + '&btnG='
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    time.sleep(random.randrange(5, 15))
    return soup.text

def clean_response(row):
    response = google(row)
    #response += scholar(row)
    if response: 
        first_name = row['firstname']
        last_name = row['name']
        response = response.replace(f'{first_name}+{last_name}+digital+humanities',' ').replace('Google Search×Please click here if you are not redirected within a few seconds.    AllNewsImagesVideos Maps Shopping Books Search tools    Any timeAny timePast hourPast 24 hoursPast weekPast monthPast yearAll resultsAll resultsVerbatim','')
        response = response.replace(f'{first_name}','').replace(f'{last_name}',' ')
        if "This page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the Terms of Service." in response:
            #stop script
            print('[-] Google blocked us')
            exit()
        pbar.update(1)
        return response
    
reviewer_df['info'] = reviewer_df.apply(clean_response, axis=1)
reviewer_df.to_csv('reviewers2.csv')






