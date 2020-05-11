import requests
import xml.etree.ElementTree as ET
import urllib
from newspaper import Article
import pandas as pd
import time
import sys

keywords = pd.read_excel(sys.argv[1], header=0)
excluded_link = pd.read_excel('irrelevant_links.xlsx', header=0, encoding='utf-8')
extract_data={'keyword':[], 'title':[], 'publish_date':[], 'content':[], 'summary':[], 'article_link':[]}

# function to extract hourly data

# def getNewsByHours(url, key):
#     mytree=ET.parse(urllib.request.urlopen(url))
#     root=mytree.getroot()
#     for x in root.iter('item'):
#       if x.find('source').attrib['url'] not in excluded_list:
#            extract_data['keyword'].append(key)
#            extract_data['title'].append(x.find('title').text)
#            extract_data['article_link'].append(x.find('link').text)
#            extract_data['publish_date'].append(x.find('pubDate').text)

# function to extract daily data

def getNewsByDays(url, key):
    mytree=ET.parse(urllib.request.urlopen(url))
    root=mytree.getroot()
    excluded_list = excluded_link.Links.tolist()
    for x in root.iter('item'):
        if x.find('source').attrib['url'] not in excluded_list:
            extract_data['keyword'].append(key)
            extract_data['title'].append(x.find('title').text)
            extract_data['article_link'].append(x.find('link').text)
            extract_data['publish_date'].append(x.find('pubDate').text)

# function to extract data from article websites        

def getData():
    for link in extract_data['article_link']:
        try:
            article=Article(link)
            article.download()
            article.parse()
            article.nlp()
            extract_data['content'].append(article.text)
            extract_data['summary'].append(article.summary)
        except:
            extract_data['content'].append('')
            extract_data['summary'].append('') 

date=1
# hour=1
urlDaily=f"https://news.google.com/rss/search?q=covid%20when%3A1d&hl=en-IN&gl=IN&ceid=IN:en"
getNewsByDays(urlDaily, 'covid')
time.sleep(1)
    
#     use this code when extracting on hourly basis
#     urlHourly=f"https://news.google.com/rss/search?q={keyword}%20when%3A{hour}h&hl=en-IN&gl=IN&ceid=IN:en"
#     getNewsByHours(urlHourly, key)

getData()

name=sys.argv[2]
pd.DataFrame(extract_data).to_excel(f'{name}.xlsx', index=False, encoding='utf-8') 