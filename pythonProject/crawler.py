from urllib.request import urlopen

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


html = urlopen("https://m.cafe.daum.net/?t__nil_gnb=home")
bsObject = BeautifulSoup(html, "html.parser")
title_list = bsObject.find_all("strong", {"class": "popular-list__title"})
href_list = bsObject.find_all("a", {"class": "popular-list__link"})
for title in title_list:
    print(title.text)
for link in href_list:
    print(link.get("href"))





