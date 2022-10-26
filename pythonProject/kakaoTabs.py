def kakaoviewTabList():
    try:
        resultList = [  "실시간 뉴스",
                        "경제",
                        "시선이 담긴 이슈",
                        "취미",
                        "사는 이야기",
                        "커리어",
                        "브랜드 스토리",
                        "지식교양",
                        "스포츠",
                        "오늘 뭐볼까",
                        "연예",
                        "패션 뷰티",
                        "리빙",
                        "건강",
                        "푸드",
                        "테크",
                        "아트",
                        "반려 생활",
                        "유머",
                        "여행",
                        "쇼핑 정보",
                        "교육",
                        "자동차",
                        "실시간검색어(네이버)"
                      ]
    except:
        resultList=[]

    return resultList

def siteList():
    resultList = [  "NAVER",
                    "FM코리아",
                    "Daum"
                  ]
    return resultList

def findkakaoTab(gubn):
    tab = { "실시간 뉴스":"01",
            "경제":"02",
            "시선이 담긴 이슈":"03",
            "취미":"04",
            "사는 이야기":"05",
            "커리어":"06",
            "브랜드 스토리":"07",
            "지식교양":"08",
            "스포츠":"09",
            "오늘 뭐볼까":"10",
            "연예":"11",
            "패션 뷰티":"12",
            "리빙":"13",
            "건강":"14",
            "푸드":"15",
            "테크":"16",
            "아트":"17",
            "반려 생활":"18",
            "유머":"19",
            "여행":"20",
            "쇼핑 정보":"21",
            "교육":"22",
            "자동차":"23",
            "실시간검색어(네이버)": "24",
            }.get(gubn, "")
    return tab

def setBaseInfo(inputText, webGubn):
    if   inputText == "실시간 뉴스":
        result = setWebInfo(webGubn, "01")
    elif inputText == "경제":
        result = setWebInfo(webGubn, "02")
    elif inputText == "시선이 담긴 이슈":
        result = setWebInfo(webGubn, "03")
    elif inputText == "취미":
        result = setWebInfo(webGubn, "04")
    elif inputText == "사는 이야기":
        result = setWebInfo(webGubn, "05")
    elif inputText == "커리어":
        result = setWebInfo(webGubn, "06")
    elif inputText == "브랜드 스토리":
        result = setWebInfo(webGubn, "07")
    elif inputText == "지식교양":
        result = setWebInfo(webGubn, "08")
    elif inputText == "스포츠":
        result = setWebInfo(webGubn, "09")
    elif inputText == "오늘 뭐볼까":
        result = setWebInfo(webGubn, "10")
    elif inputText == "연예":
        result = setWebInfo(webGubn, "11")
    elif inputText == "패션 뷰티":
        result = setWebInfo(webGubn, "12")
    elif inputText == "리빙":
        result = setWebInfo(webGubn, "13")
    elif inputText == "건강":
        result = setWebInfo(webGubn, "14")
    elif inputText == "푸드":
        result = setWebInfo(webGubn, "15")
    elif inputText == "테크":
        result = setWebInfo(webGubn, "16")
    elif inputText == "아트":
        result = setWebInfo(webGubn, "17")
    elif inputText == "반려 생활":
        result = setWebInfo(webGubn, "18")
    elif inputText == "유머":
        result = setWebInfo(webGubn, "19")
    elif inputText == "여행":
        result = setWebInfo(webGubn, "20")
    elif inputText == "쇼핑 정보":
        result = setWebInfo(webGubn, "21")
    elif inputText == "교육":
        result = setWebInfo(webGubn, "22")
    elif inputText == "자동차":
        result = setWebInfo(webGubn, "23")
    elif inputText == "실시간검색어(네이버)":
        result = setWebInfo(webGubn, "24")
    return result

def setWebInfo(webGubn, gubnTag):
    if   webGubn == "NAVER":
        webUrl = setNaverSite(gubnTag)
    elif webGubn == "FM코리아":
        webUrl = fmKoreaSite(gubnTag)
    elif webGubn == "Daum":
        webUrl = daum_site(gubnTag)

    siteInfo = {"siteUrl": webUrl, "tagCd": gubnTag}
    return siteInfo

def setNaverSite(gubnTag):
    if   gubnTag == "01":
        result = "https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111"
    elif gubnTag == "02":
        result = ""
    elif gubnTag == "03":
        result = ""
    elif gubnTag == "04":
        result = ""
    elif gubnTag == "05":
        result = ""
    elif gubnTag == "06":
        result = ""
    elif gubnTag == "07":
        result = ""
    elif gubnTag == "08":
        result = ""
    elif gubnTag == "09":
        result = ""
    elif gubnTag == "10":
        result = ""
    elif gubnTag == "11":
        result = ""
    elif gubnTag == "12":
        result = ""
    elif gubnTag == "13":
        result = ""
    elif gubnTag == "14":
        result = ""
    elif gubnTag == "15":
        result = ""
    elif gubnTag == "16":
        result = ""
    elif gubnTag == "17":
        result = ""
    elif gubnTag == "18":
        result = ""
    elif gubnTag == "19":
        result = "https://m.bboom.naver.com/best/moreList.json?viewTypeNo=2&limit=0&length=1000"
    elif gubnTag == "20":
        result = ""
    elif gubnTag == "21":
        result = ""
    elif gubnTag == "22":
        result = ""
    elif gubnTag == "23":
        result = "https://www.naver.com/nvhaproxy/v1/panels/CARGAME/html"
    elif gubnTag == "24":
        result = "https://api.signal.bz/news/realtime"
    return result

def fmKoreaSite(gubnTag):
    if   gubnTag == "01":
        result = ""
    elif gubnTag == "02":
        result = ""
    elif gubnTag == "03":
        result = "https://www.fmkorea.com/humor"
    elif gubnTag == "04":
        result = ""
    elif gubnTag == "05":
        result = ""
    elif gubnTag == "06":
        result = ""
    elif gubnTag == "07":
        result = ""
    elif gubnTag == "08":
        result = ""
    elif gubnTag == "09":
        result = ""
    elif gubnTag == "10":
        result = ""
    elif gubnTag == "11":
        result = ""
    elif gubnTag == "12":
        result = ""
    elif gubnTag == "13":
        result = ""
    elif gubnTag == "14":
        result = ""
    elif gubnTag == "15":
        result = ""
    elif gubnTag == "16":
        result = ""
    elif gubnTag == "17":
        result = ""
    elif gubnTag == "18":
        result = ""
    elif gubnTag == "19":
        result = "https://www.fmkorea.com/humor"
    elif gubnTag == "20":
        result = ""
    elif gubnTag == "21":
        result = ""
    elif gubnTag == "22":
        result = ""
    elif gubnTag == "23":
        result = ""
    return result

def daum_site(gubnTag):
    if   gubnTag == "01":
        result = "https://news.daum.net/"
    elif gubnTag == "02":
        result = ""
    elif gubnTag == "03":
        result = ""
    elif gubnTag == "04":
        result = ""
    elif gubnTag == "05":
        result = ""
    elif gubnTag == "06":
        result = ""
    elif gubnTag == "07":
        result = ""
    elif gubnTag == "08":
        result = ""
    elif gubnTag == "09":
        result = ""
    elif gubnTag == "10":
        result = ""
    elif gubnTag == "11":
        result = ""
    elif gubnTag == "12":
        result = ""
    elif gubnTag == "13":
        result = ""
    elif gubnTag == "14":
        result = ""
    elif gubnTag == "15":
        result = ""
    elif gubnTag == "16":
        result = ""
    elif gubnTag == "17":
        result = ""
    elif gubnTag == "18":
        result = ""
    elif gubnTag == "19":
        result = "https://m.cafe.daum.net/?t__nil_gnb=home"
    elif gubnTag == "20":
        result = ""
    elif gubnTag == "21":
        result = ""
    elif gubnTag == "22":
        result = ""
    elif gubnTag == "23":
        result = ""
    return result

def somethingElseSite(gubnTag):
    if   gubnTag == "01":
        result = ""
    elif gubnTag == "02":
        result = ""
    elif gubnTag == "03":
        result = ""
    elif gubnTag == "04":
        result = ""
    elif gubnTag == "05":
        result = ""
    elif gubnTag == "06":
        result = ""
    elif gubnTag == "07":
        result = ""
    elif gubnTag == "08":
        result = ""
    elif gubnTag == "09":
        result = ""
    elif gubnTag == "10":
        result = ""
    elif gubnTag == "11":
        result = ""
    elif gubnTag == "12":
        result = ""
    elif gubnTag == "13":
        result = ""
    elif gubnTag == "14":
        result = ""
    elif gubnTag == "15":
        result = ""
    elif gubnTag == "16":
        result = ""
    elif gubnTag == "17":
        result = ""
    elif gubnTag == "18":
        result = ""
    elif gubnTag == "19":
        result = ""
    elif gubnTag == "20":
        result = ""
    elif gubnTag == "21":
        result = ""
    elif gubnTag == "22":
        result = ""
    elif gubnTag == "23":
        result = ""
    return result