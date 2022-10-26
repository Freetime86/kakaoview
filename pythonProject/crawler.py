from urllib.request import urlopen
import urllib
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys
import os
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/'
#                         '537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#data = requests.get('https://www.genie.co.kr/chart/top200?ditc=M&rtm=N&ymd=20210701', headers=headers)
#soup = BeautifulSoup(data.text, 'html.parser')

#musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#soup.find('span', class_='icon icon-19').decompose()

#sel_year = sel_date[0:4]

#html = urlopen("https://api.signal.bz/news/realtime")
response = requests.get("https://api.signal.bz/news/realtime")
data = json.loads(response.text)
keyword_list = data['top10']

link_list = []
head_list = []
for word in keyword_list:
    keyword = word['keyword']
    encoded_keyword = urllib.parse.quote(keyword)
    html = urlopen("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=" + encoded_keyword)
    bsObject = BeautifulSoup(html, "html.parser")
    print(bsObject.find_all('a'))
    a_list = bsObject.find_all('a', {'class': 'news_tit'})
    sub_list = bsObject.find_all('a', {'class': 'sub_tit'})
    for link in a_list:
        head_list.append(link.text)
        link_list.append(link.get('href'))

    for link in sub_list:
        head_list.append(link.text)
        link_list.append(link.get('href'))







