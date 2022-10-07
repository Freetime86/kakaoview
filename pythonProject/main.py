from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup
import time
import filterWords
import supportModule
import kakaoTabs
import parsingModule


def main_process(dataset):
    # 입력정보 변수 선언
    sel_tab = dataset['sel_tab']  # 카카오탭 태그
    sel_site = dataset['sel_site']  # 크롤링 타겟 웹사이트
    user_id = dataset['user_id']  # 입력 유저
    user_pw = dataset['user_pw']  # 유저 패스워드
    sel_date = dataset['sel_date']  # 발행 지정일
    sel_hour = dataset['sel_hour']  # 시작 시간
    sel_min = dataset['sel_min']  # 시작 분
    jump_time = dataset['jump_time']  # 발행 간격
    out_list_arr = dataset['except_list']  # 제외 아이디
    srt_seq = dataset['srt_seq']  # 시작 시퀸스
    loop_cnt = dataset['loop_cnt']  # 발행 갯수
    include_yn = dataset['include_yn']  # 채널목록 채널 발행 포함 유무 Y:채널목록포함 나머진 제외 N:채널목록제외 나머진 포함
    static_title = dataset['static_title']  # 채널 공통 고정 제목 기사의 제목은 컨텐츠 내용에 기재한다.

    # 기본정보 세팅
    target_info = kakaoTabs.setBaseInfo(sel_tab, sel_site)
    target_url = target_info['siteUrl']
    target_gubn = target_info['tagCd']

    # 필터링
    check_list = filterWords.filter_list()

    # 타켓 웹 정보
    html = urlopen(target_url)
    bs_object = BeautifulSoup(html, "html.parser")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 300)
    url = "https://creators.kakao.com/my-channels/"
    driver.get(url)
    driver.maximize_window()

    # 계정 로그인
    wait.until(EC.visibility_of_element_located((By.ID, "id_email_2"))).send_keys(user_id)
    wait.until(EC.visibility_of_element_located((By.ID, "id_password_3"))).send_keys(user_pw)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn_g"))).click()

    time.sleep(7)

    # 채널 리스트 뽑기
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'link_channel')))
    channel_arr = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.list_channel li>a.link_channel")))

    # 채널 SEQ 생성
    index = 0

    # 제외채널 포함 교정 index
    fix_index = 0

    # 타겟row 인덱스 때문에 입력을 1로 받고 0번 인덱스부터 인식하도록 -1 조정한다
    target_row = int(srt_seq)
    target_board_cnt = 0

    while index < len(channel_arr):

        channel = \
            wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.list_channel li>a.link_channel")))[
                index]
        channel_id = channel.find_element(By.CSS_SELECTOR, "strong.tit_channel").text

        print("채널 순번 (사이트 기준) : " + str(index + 1) + " (" + channel_id + ")")

        # 제외 채널 여부
        if include_yn == "Y":
            is_validate = False
        else:
            is_validate = True
        for outChannel in out_list_arr:
            # 매칭된 채널은 제외한다.
            if include_yn == "N":
                if channel_id.find(outChannel) == 0:
                    is_validate = False
                    print("채널 제외 대상! (KEY : " + outChannel + ") : " + channel_id)
                    fix_index = fix_index - 1
                    break

            # 매칭된 채널만 추가한다.
            elif include_yn == "Y":
                if channel_id.find(outChannel) == 0:
                    is_validate = True

        if include_yn == "Y" and is_validate == False:
            print("채널 제외 대상! (KEY : " + channel_id + ") : " + channel_id)
            fix_index = fix_index - 1

        # board_share_succ = False
        if is_validate:
            channel.click()

            # 마지막 발행된 8개 보드
            last_his_board_list = driver.find_elements(By.CSS_SELECTOR, "ul.list_board a.tit_board")
            last_board_list = []
            for board in last_his_board_list:
                last_board_list.append(board.text)

            now = int(sel_hour)

            sel_day = sel_date[6:8]
            sel_mon = sel_date[4:6]
            sel_year = sel_date[0:4]
            current_date = datetime.now().strftime("%Y%m%d")

            month_cnt = 0
            # 캘린더 세팅 계산
            # 선택된 년도가 현재 년도보다 이후라면
            if int(sel_year) > int(current_date[0:4]):
                # 선택된 달이 현재 달보다 크다면 차이 값 계산
                if int(sel_mon) >= int(current_date[4:6]):
                    month_cnt = int(sel_mon) - int(current_date[4:6])
                else:
                    month_cnt = (int(sel_mon) + 12) - int(current_date[4:6])
            else:
                # 선택된 달이 현재 달보다 크다면 차이 값 계산
                if int(sel_mon) > int(current_date[4:6]):
                    month_cnt = int(sel_mon) - int(current_date[4:6])

            is_next_day = 0
            # 시간 때 별로 2시간 단위 오전 04시 ~ 오후 22시 까지 총 10개 제작
            # 채널 통과 하였을 시 누적되는 index * 10 카운팅에 대한 교정 index 수식
            final_cnt = int(loop_cnt) * (1 + index + fix_index)

            while target_board_cnt < final_cnt:

                print("현재 내 채널 보드 발행 갯수 : " + str(target_board_cnt + 1))

                # 보드탭 이동 후 보드 만들기
                if (target_board_cnt % int(loop_cnt)) == 0:
                    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.list_snb li>a.link_snb")))[
                        1].click()

                time.sleep(0.5)

                # 보드 만들기
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.group_etc a.btn_g"))).click()
                # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'link_newboard'))).click()

                # 보드 최송 발행 진행 여부
                activation = True

                data = parsingModule.parseData(target_gubn, sel_site, target_row, bs_object)

                # 변동이 생겼을 경우를 대비해 override
                target_row = data['rowIdx']
                title = filterWords.text_incoding(data['title'])
                link = data['link']
                target_cnt = int(data['dataCnt'])

                # 악성단어 체크
                if not supportModule.filterWords(check_list, title):
                    activation = False
                    while not activation:
                        target_row = target_row + 1
                        data = parsingModule.parseData(target_gubn, sel_site, target_row, bs_object)

                        # 변동이 생겼을 경우를 대비해 override
                        target_row = data['rowIdx']
                        title = data['title']
                        link = data['link']
                        target_cnt = int(data['dataCnt'])

                        if target_row > target_cnt:
                            print("추출 보드 데이터보다 보드 발행 수가 초과하여 정지되었습니다.")
                            return

                        # 악성단어 걸러지는 데이터가 추출될 때 까지 반복
                        if supportModule.filterWords(check_list, title):
                            activation = True

                # 발행 보드 포함 여부
                if not supportModule.compareboard(last_board_list, title):
                    activation = False

                # 총 추출 카운팅보다 크면 보드발행금지!
                if target_row <= target_cnt:
                    # 보드발행
                    if activation:

                        print("Data 추가 현황 : " + str(target_row + 1) + "/" + str(target_cnt))

                        time.sleep(0.5)

                        # 링크탭 활성화
                        # driver.find_elements(By.CSS_SELECTOR, "ul.list_tab li>a.link_tab")[1].click()
                        wait.until(
                            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.list_tab li>a.link_tab")))[
                            1].click()

                        # 링크입력
                        wait.until(EC.visibility_of_element_located((By.NAME, "url"))).send_keys(link)

                        # 링크검색
                        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn_search"))).click()

                        # 담기
                        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn_tertiary_round"))).click()

                        # 고정 제목
                        # wait.until(EC.visibility_of_element_located((By.ID, "boardTitle"))).send_keys(static_title)
                        wait.until(EC.visibility_of_element_located((By.ID, "boardTitle"))).send_keys(title)
                        # 기사 제목
                        # wait.until(EC.visibility_of_element_located((By.ID, "boardCmt"))).send_keys(title)

                        # 발행
                        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn_primary"))).click()

                        share_now = "N"
                        # 발행시점 예약 발행 현재 예약 선택 2번선택 3번 예약
                        wait.until(EC.visibility_of_all_elements_located(
                            (By.CSS_SELECTOR, "label.lab_choice span.ico_radio")))[
                            3].click()

                        if share_now == "N":
                            # time.sleep(1)
                            # 자정을 넘기면 멈춘다.
                            # 추후 추가 기능 개발 예정으로 일단 리턴처리
                            if now >= 24:
                                return
                                is_next_day = 1
                                # 24시간을 넘기면 날짜 변경
                                driver.find_element(By.CLASS_NAME, "DayPickerInput").click()

                                for calDay in driver.find_elements(By.CLASS_NAME, "DayPicker-Day"):
                                    if calDay.text == str(today + is_next_day):
                                        calDay.click()
                                        # 오전 4시부터 발행시작 2시간 단위
                                        now = 4
                                        time.sleep(0.5)
                                        break

                            # 하루 지났으면
                            # 추가 개발예정 일단 죽임 위에서 next day counting 이 올라가지 않아서 죽은 기능 사실상
                            if is_next_day > 0:
                                driver.find_element(By.CLASS_NAME, "DayPickerInput").click()
                                for calDay in driver.find_elements(By.CLASS_NAME, "DayPicker-Day"):
                                    if calDay.text == str(today + is_next_day):
                                        calDay.click()
                                        time.sleep(0.5)
                                        break

                            # 현재 이 기능으로 date select 값으로 현재 일자 지정
                            driver.find_element(By.CLASS_NAME, "DayPickerInput").click()

                            for i in range(0, month_cnt):
                                driver.find_elements(By.CLASS_NAME, "DayPicker-NavButton")[1].click()

                            for calDay in driver.find_elements(By.CLASS_NAME, "DayPicker-Day"):
                                if len(calDay.text) < 2:
                                    new_cal_date = "0" + str(calDay.text)
                                if new_cal_date == str(sel_day):
                                    calDay.click()
                                    break

                            # 시간 때 선택
                            # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "link_selected"))).click()
                            # 현재 시간에 맞는 시간 세팅
                            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "link_selected")))
                            time.sleep(0.3)
                            driver.find_elements(By.CLASS_NAME, "link_selected")[0].click()
                            wait.until(EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "div.opt_open div.box_opt ul.list_opt li")))
                            driver.find_elements(By.CSS_SELECTOR, "div.opt_open div.box_opt ul.list_opt li")[
                                now].click()

                            # time.sleep(1)

                            # 분은 정시로 초기화
                            time.sleep(0.3)
                            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "link_selected")))
                            driver.find_elements(By.CLASS_NAME, "link_selected")[1].click()
                            # time.sleep(0.3)
                            # time.sleep(0.3)
                            wait.until(EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "div.opt_open div.box_opt ul.list_opt li")))
                            driver.find_elements(By.CSS_SELECTOR, "div.opt_open div.box_opt ul.list_opt li")[
                                int(sel_min[0:1])].click()

                        # 이슈선택
                        sel_tag = sel_tab
                        tag_arr = driver.find_elements(By.CSS_SELECTOR, "div.type_text2 label.lab_choice")
                        for tag in tag_arr:
                            if tag.text == sel_tag:
                                tag.click()

                        # 발행
                        driver.find_element(By.CSS_SELECTOR, "div.inner_layer div.wrap_btn button.btn_primary").click()
                        # time.sleep(0.5)

                        # 발행완료 버튼 대기 후 클릭
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                   "div.inner_layer div.layer_foot div.wrap_btn button.btn_primary"))).click()

                        # 진행을 했던 안했던 어떤 이유에서 현재 타겟의 row는 지나갔기에 카운팅을 올림
                        # 보드발행을 진행하지 않을 경우는 올리지 않음
                        target_row = target_row + 1
                        now = now + int(jump_time)

                    # 현재 추출된URL 리스트 카운팅 현황을 체크
                    target_board_cnt = target_board_cnt + 1
                else:
                    print("추출 보드 데이터보다 보드 발행 수가 초과하여 정지되었습니다.")
                    return
            board_share_succ = True

            driver.find_elements(By.CSS_SELECTOR, "ul.list_gnb li>a.link_gnb")[0].click()
            time.sleep(0.5)

        # 채널 시퀸스
        index = index + 1

    return
    # while True:
    #    pass
