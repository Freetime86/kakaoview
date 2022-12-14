import urllib
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup


open_flag = False
parsing_head = []
parsing_link = []

def index_validation(targetlist, targetRow):
    result = True
    list_cnt = len(targetlist)
    if list_cnt < targetRow:
        print('No Data exists. TARGET : ' + str(list_cnt) + ' / CURRENT : ' + str(targetRow))
        print('Working is stoped!!')
        result = False
    return result

def parseData(targetGubn, selectSite, targetRow, bsObj):
    result = ""
    targetlist = []
    targetRow = int(targetRow)
    if selectSite == "NAVER":
        if targetGubn == "01":
            targetlist = bsObj.find_all('a', {'class': 'list_title'})

            if not index_validation(targetlist, targetRow):
                return

            news = targetlist[targetRow]

            current_title = news.text
            current_link = news.get('href')
        elif targetGubn == "02":
            return
        elif targetGubn == "03":
            return
        elif targetGubn == "04":
            return
        elif targetGubn == "05":
            return
        elif targetGubn == "06":
            return
        elif targetGubn == "07":
            return
        elif targetGubn == "08":
            return
        elif targetGubn == "09":
            return
        elif targetGubn == "10":
            return
        elif targetGubn == "11":
            return
        elif targetGubn == "12":
            return
        elif targetGubn == "13":
            return
        elif targetGubn == "14":
            return
        elif targetGubn == "15":
            return
        elif targetGubn == "16":
            return
        elif targetGubn == "17":
            return
        elif targetGubn == "18":
            return
        elif targetGubn == "19":
            for li in bsObj.find_all("li", {'class': 'check_visible claim'}):
                li.decompose()

            targetlist = bsObj.select('li.check_visible > div._child_wrapper > span.info > strong.tit')
            url_list = bsObj.select('li.check_visible > div._child_wrapper > span.info > a.link')

            if not index_validation(targetlist, targetRow):
                return
            
            title_arr = []
            for title in targetlist:
                title_arr.append(title.text)

            url_arr = []
            for url in url_list:
                href = url.get('href').replace('amp;', '')
                url_arr.append('https://m.bboom.naver.com' + href)

            current_title = title_arr[targetRow]
            current_link = url_arr[targetRow]

        elif targetGubn == "20":
            return
        elif targetGubn == "21":
            return
        elif targetGubn == "22":
            return
        elif targetGubn == "23":

            targetlist = bsObj.find_all('a', {'class': 'theme_thumb'})
            if not index_validation(targetlist, targetRow):
                return

            current_title = bsObj.find_all('a', {'class': 'theme_thumb'})[targetRow].select('img')[0]['alt']
            current_link = bsObj.find_all('a', {'class': 'theme_thumb'})[targetRow].get('href')

        #????????? ????????? ?????? BS_OBJECT ??? ?????? API ????????? ?????????.
        elif targetGubn == "24":

            global open_flag
            global parsing_head
            global parsing_link

            if not open_flag:
                response = requests.get("https://api.signal.bz/news/realtime")
                data = json.loads(response.text)
                keyword_list = data['top10']

                link_list = []
                head_list = []
                for word in keyword_list:
                    keyword = word['keyword']
                    encoded_keyword = urllib.parse.quote(keyword)
                    html = urlopen(
                        "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=" + encoded_keyword)
                    bsObject = BeautifulSoup(html, "html.parser")
                    a_list = bsObject.find_all('a', {'class': 'news_tit'})
                    sub_list = bsObject.find_all('a', {'class': 'sub_tit'})
                    for link in a_list:
                        head_list.append(link.text)
                        link_list.append(link.get('href'))

                    for link in sub_list:
                        head_list.append(link.text)
                        link_list.append(link.get('href'))
                parsing_head = head_list
                parsing_link = link_list

                open_flag = True
            current_title = parsing_head[targetRow]
            current_link = parsing_link[targetRow]
            targetlist = parsing_head

    elif selectSite == "FM?????????":
        if targetGubn == "01":
            return
        elif targetGubn == "02":
            return
        elif targetGubn == "03":
            return
        elif targetGubn == "04":
            return
        elif targetGubn == "05":
            return
        elif targetGubn == "06":
            return
        elif targetGubn == "07":
            return
        elif targetGubn == "08":
            return
        elif targetGubn == "09":
            return
        elif targetGubn == "10":
            return
        elif targetGubn == "11":
            return
        elif targetGubn == "12":
            return
        elif targetGubn == "13":
            return
        elif targetGubn == "14":
            return
        elif targetGubn == "15":
            return
        elif targetGubn == "16":
            return
        elif targetGubn == "17":
            return
        elif targetGubn == "18":
            return
        elif targetGubn == "19":
            titleArr = bsObj.find_all('div', {'class': 'wtitle'})

            # ?????? ????????? ?????? ?????? ????????? ??? ????????? break????????? stop
            tag = "??????"
            targetIdx = 0
            for idx, title in enumerate(titleArr):
                if not title.find('a').text.find(tag) == -1:
                    targetIdx = idx
                    break

            headUrl = "https://www.fmkorea.com/index.php?mid=humor&sort_index=pop&order_type=desc&document_srl="
            targetlist = bsObj.find_all('ul', {'class': 'mpReset'})
            humorList = targetlist[targetIdx].find_all('a')

            if not index_validation(targetlist, targetRow):
                return

            humor = humorList[targetRow]

            # ?????? a ?????? ??????
            if "#comment" not in humor.get('href'):
                current_title = humor.text
                current_link = headUrl + humor.get('href').replace("/", "")
                targetRow = targetRow + 1

        elif targetGubn == "20":
            return
        elif targetGubn == "21":
            return
        elif targetGubn == "22":
            return
        elif targetGubn == "23":
            return

    elif selectSite == "Daum":
        if targetGubn == "01":
            targetlist = bsObj.find_all('div', {'class': 'cont_thumb'})

            if not index_validation(targetlist, targetRow):
                return

            news = targetlist[targetRow]

            current_title = news.select('a')[0].text
            current_link = news.select('a')[0].get('href')

        elif targetGubn == "02":
            return
        elif targetGubn == "03":
            return
        elif targetGubn == "04":
            return
        elif targetGubn == "05":
            return
        elif targetGubn == "06":
            return
        elif targetGubn == "07":
            return
        elif targetGubn == "08":
            return
        elif targetGubn == "09":
            return
        elif targetGubn == "10":
            return
        elif targetGubn == "11":
            return
        elif targetGubn == "12":
            return
        elif targetGubn == "13":
            return
        elif targetGubn == "14":
            return
        elif targetGubn == "15":
            return
        elif targetGubn == "16":
            return
        elif targetGubn == "17":
            return
        elif targetGubn == "18":
            return
        elif targetGubn == "19":
            targetlist = bsObj.find_all("strong", {"class": "popular-list__title"})
            url_list = bsObj.find_all("a", {"class": "popular-list__link"})
            if not index_validation(targetlist, targetRow):
                return

            title_arr = []
            for title in targetlist:
                title_arr.append(title.text)

            url_arr = []
            for url in url_list:
                href = url.get('href')
                url_arr.append('https://m.cafe.daum.net' + href)

            current_title = title_arr[targetRow]
            current_link = url_arr[targetRow]
        elif targetGubn == "20":
            return
        elif targetGubn == "21":
            return
        elif targetGubn == "22":
            return
        elif targetGubn == "23":
            return

    elif selectSite == "xxxxx":
        if targetGubn == "01":
            return
        elif targetGubn == "02":
            return
        elif targetGubn == "03":
            return
        elif targetGubn == "04":
            return
        elif targetGubn == "05":
            return
        elif targetGubn == "06":
            return
        elif targetGubn == "07":
            return
        elif targetGubn == "08":
            return
        elif targetGubn == "09":
            return
        elif targetGubn == "10":
            return
        elif targetGubn == "11":
            return
        elif targetGubn == "12":
            return
        elif targetGubn == "13":
            return
        elif targetGubn == "14":
            return
        elif targetGubn == "15":
            return
        elif targetGubn == "16":
            return
        elif targetGubn == "17":
            return
        elif targetGubn == "18":
            return
        elif targetGubn == "19":
            return
        elif targetGubn == "20":
            return
        elif targetGubn == "21":
            return
        elif targetGubn == "22":
            return
        elif targetGubn == "23":
            return

    # ?????? ?????? ??? ??????
    dataCnt = len(targetlist)
    result = {"title": str(current_title), "link": str(current_link), "rowIdx": targetRow, "dataCnt": dataCnt}
    return result

