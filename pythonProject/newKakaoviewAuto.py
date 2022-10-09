import pyautogui
from datetime import datetime, timedelta
import os
import time


def win_activate(dataset):
    window = pyautogui.getWindowsWithTitle(dataset['win_title'])[0]
    window.activate()


def find_location(dataset):
    work_dir = os.getcwd() + "\img"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        print("find_location : " + file_name + dataset['filename_option'] + file_ext)
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=float(dataset['accuracy']))
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def find_location_accuracy(dataset, accuracy):
    work_dir = os.getcwd() + "\img"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        # print("find_location : " + file_name + dataset['filename_option'] + file_ext)
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=accuracy)
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def find_loading_status(dataset, accuracy):
    work_dir = os.getcwd() + "\img"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        print("find_location : " + file_name + dataset['filename_option'] + file_ext)
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=accuracy, region=(0, 100, 150, 400))
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def is_board(dataset):
    dataset['file_name_list'] = ['\main_board_txt']
    board_txt = find_location_accuracy(dataset, 0.80)

    result = False
    for loc in board_txt:
        this_loc = pyautogui.center(loc)
        if this_loc.y < 150:
            result = True
    return result


def is_loaded(dataset):
    dataset['file_name_list'] = dataset['loading_img_list']
    loading_bar = find_location_accuracy(dataset, 0.90)

    if not dataset['loading_msg']:
        print('로딩 중..')
        dataset['loading_msg'] = True
    result = True
    for loc in loading_bar:
        this_loc = pyautogui.center(loc)
        if 150 > this_loc.y > 100 and 450 > this_loc.x > 0:
            result = False

    if result:
        dataset['loading_msg'] = False
    return result


def timeout(dataset):
    timeout = datetime.now() + timedelta(seconds=float(dataset['limit_time']))
    return timeout


def check_timeout(timeout):
    result = True
    if timeout < datetime.now():
        result = False
    return result


def scroll_down(dataset):
    print("scroll_down")
    next_step = False
    scroll_loc = (18, 931)
    pyautogui.click(scroll_loc)
    time.sleep(float(dataset['speed']))
    set_time_out = timeout(dataset)
    timeout_flag = False

    while not next_step:

        if dataset['is_refresh']:
            pyautogui.click(scroll_loc)
            time.sleep(float(dataset['speed']))
            dataset['is_refresh'] = False

        dataset['file_name_list'] = ['\scroll_down']
        scroll_down_icon = find_location(dataset)

        if check_timeout(set_time_out):
            if len(scroll_down_icon) > 0 and not timeout_flag:
                timeout_flag = True
                scroll_down_loc = pyautogui.center(scroll_down_icon[0])

                for i in range(1, int(dataset['scroll_count'])):
                    pyautogui.click(scroll_down_loc)
                    time.sleep(1)

                dataset['file_name_list'] = ['\scroll_close']
                scroll_close = find_location(dataset)

                if len(scroll_close) > 0:
                    scroll_close_loc = pyautogui.center(scroll_close[0])
                    pyautogui.moveTo(scroll_close_loc)
                    pyautogui.mouseDown()
                    pyautogui.moveTo(5, scroll_close_loc.y)
                    pyautogui.mouseUp()
                    # time.sleep(float(dataset['speed']))

                    is_capture = False
                    while not next_step:
                        if not is_capture:
                            next_step = capture_back(dataset)
                            if next_step:
                                is_capture = True
        else:
            print("스크롤 찾기 실패")
            if set_time_out < datetime.now():
                print('리프레쉬2 리로드')
                refresh_reload(dataset)
                timeout_flag = False
                set_time_out = timeout(dataset)
    return next_step


# 캡처 후 이전 process 로 복귀
def capture_back(dataset):
    print("capture_back")
    next_step = False
    return_my_view = dataset['return_my_view']
    dataset['file_name_list'] = ['\capture', '\capture1']
    capture_icon = find_location(dataset)
    if len(capture_icon) > 0:

        is_capture = False
        while not is_capture:
            if is_loaded(dataset):
                capture_loc = pyautogui.center(capture_icon[0])
                pyautogui.click(capture_loc)
                time.sleep(float(dataset['speed']))
                is_capture = True

        if return_my_view:
            print("마이뷰로 돌아가기")
            while not next_step:

                dataset['file_name_list'] = ['\capture_back', '\capture_back1']
                my_view_return = find_location(dataset)

                if len(my_view_return) > 0:
                    my_view_return_loc = pyautogui.center(my_view_return[0])
                    set_time_out = timeout(dataset)
                    timeout_flag = False
                    first_try = True
                    try_count = 0
                    while not next_step:
                        if check_timeout(set_time_out):
                            if not timeout_flag:
                                if try_count == 3:
                                    for index in range(1, try_count):
                                        if not is_board(dataset):
                                            pyautogui.click(my_view_return_loc)
                                            try_count = 0
                                else:
                                    if first_try:
                                        pyautogui.click(my_view_return_loc)
                                        first_try = False
                                        time.sleep(1)
                                    pyautogui.click(my_view_return_loc)
                                    try_count = try_count + 1
                                timeout_flag = True

                            dataset['file_name_list'] = ['\my_view_text']
                            my_view_text = find_location(dataset)

                            # 마이뷰 복귀 확인
                            if len(my_view_text) > 0:
                                print("마이뷰 확인")
                                next_step = True
                        else:
                            print("마이뷰 인식 실패")
                            timeout_flag = False
                            set_time_out = timeout(dataset)
        else:
            print("뒤로가기")
            while not next_step:
                dataset['file_name_list'] = ['\capture_back', '\capture_back1']
                capture_back = find_location(dataset)
                if len(capture_back) > 0:
                    capture_back_loc = pyautogui.center(capture_back[0])
                    set_time_out = timeout(dataset)
                    timeout_flag = False
                    try_count = 0
                    while not next_step:
                        if check_timeout(set_time_out):
                            if not timeout_flag:
                                if try_count == 3:
                                    for index in range(1, try_count):
                                        if not is_board(dataset):
                                            pyautogui.click(capture_back_loc)
                                            try_count = 0
                                else:
                                    pyautogui.click(capture_back_loc)
                                    try_count = try_count + 1
                                timeout_flag = True

                            # 메인 채널 여부 확인
                            if is_board(dataset):
                                next_step = True
                        else:
                            timeout_flag = False
                            set_time_out = timeout(dataset)
    return next_step


def check_loading_capture(dataset):
    print("check_loading_capture")
    next_step = False

    # 로딩바 대기 30초
    set_timeout = datetime.now() + timedelta(seconds=10)

    # 판단 근거
    # 1. 보드 텍스트가 사라진 것으로 컨텐츠 클릭으로 이동 했다고 판단
    # 2. 로딩바가 보이지 않는 시점이여야 로딩이 완료 되었다고 판단

    while not next_step:

        # 현재 위치가 보드가 아님을 판단
        if not is_board(dataset):
            print("메인채널 탈출")

            # 보드 로딩바 확인 불가 (입장 완료 또는 입장 실패) 확인 될 때까지 재실행
            loading_finish = False
            while not loading_finish:
                loading_finish = True
                next_step = scroll_down(dataset)

                # 일정 시간 후에도 기능이 동작하지 않으면 timeout (refresh)
                if not loading_finish:
                    if set_timeout < datetime.now():
                        print('리프레쉬1 리로드')
                        refresh_reload(dataset)

                        # 로딩바 대기 30초
                        set_timeout = datetime.now() + timedelta(seconds=30)
        else:
            # 일정 시간 후에도 기능이 동작하지 않으면 timeout (refresh)
            if set_timeout < datetime.now():
                print('리프레쉬2 리로드')
                refresh_reload(dataset)

                # 로딩바 대기 30초
                set_timeout = datetime.now() + timedelta(seconds=30)

    return next_step


def refresh_reload(dataset):
    print('refresh_reload')

    next_step = False
    # main channel check

    channel_main_flag = False
    while not channel_main_flag:

        if not is_board(dataset):
            # BACK BTN
            dataset['file_name_list'] = ['\capture_back', '\capture_back']
            capture_back = find_location(dataset)
            capture_back_loc = pyautogui.center(capture_back[0])
            pyautogui.doubleClick(capture_back_loc)
            time.sleep(2)
        else:
            channel_main_flag = True

    while not next_step:

        # 구글 팝업인지 체크
        dataset['file_name_list'] = ['\google_play']
        google_play = find_location_accuracy(dataset, 0.90)

        dataset['file_name_list'] = ['\google_play_x']
        google_play_x = find_location_accuracy(dataset, 0.90)

        if len(google_play) > 0 and len(google_play_x) > 0:
            print("구글팝업닫기")
            google_play_x_loc = pyautogui.center(google_play_x[0])
            pyautogui.click(google_play_x_loc)

        # 옵션 페이지 리프레시 (광고 변경)
        dataset['file_name_list'] = ['\page_refresh_option']
        board_option = find_location_accuracy(dataset, 0.80)
        if len(board_option) > 0:
            board_option_loc = pyautogui.center(board_option[0])
            pyautogui.doubleClick(board_option_loc)
            time.sleep(0.5)

            page_refresh_flag = False
            while not page_refresh_flag:
                dataset['file_name_list'] = ['\page_refresh']
                page_refresh = find_location_accuracy(dataset, 0.85)
                if len(page_refresh) > 0:
                    print("새로고침")
                    page_refresh_loc = pyautogui.center(page_refresh[0])
                    pyautogui.click(page_refresh_loc)
                    page_refresh_flag = True
                    dataset['is_refresh'] = True

            # 보드 재클릭
            time.sleep(1)
            pyautogui.click(dataset['last_location'])

            next_step = True

    return next_step


def find_heart(dataset):
    print('find_heart')
    init = dataset['start']

    next_step = False
    while not next_step:

        # My View 화면인지 세팅 아이콘으로 판단
        dataset['file_name_list'] = ['\setting_icon', '\setting_icon1']
        setting_icon = find_location_accuracy(dataset, 0.80)  # 옵션 닷 버튼 찾기

        if len(setting_icon) > 0:
            if not init:
                while not next_step:

                    win_activate(dataset)
                    # dataset['file_name_list'] = ['\option_dots', '\option_next_dots', '\option_next_dots1']
                    dataset['file_name_list'] = ['\option_dots']
                    option_dots = find_location_accuracy(dataset, '0.80')  # 옵션 닷 버튼 찾기

                    # 0은 첫번째 보드 이미 진행 완료한 건
                    # 1은 다음 보드
                    real_loc_cnt = 0
                    for location in option_dots:
                        location = pyautogui.center(location)
                        if 440 < location.y:
                            target = location
                            real_loc_cnt = real_loc_cnt + 1
                            break

                    if real_loc_cnt > 0:
                        title_loc = (target.x, target.y - 40)

                        win_activate(dataset)
                        pyautogui.moveTo(title_loc)
                        pyautogui.mouseDown()
                        setting_icon_loc = pyautogui.center(setting_icon[0])
                        setting_icon_loc = (setting_icon_loc.x, setting_icon_loc.y + 65)
                        pyautogui.moveTo(setting_icon_loc)
                        pyautogui.mouseUp()
                        next_step = True
                        time.sleep(float(dataset['speed']))
                    else:
                        print("마이뷰에서 옵션버튼 위치 찾기 실패")
                        win_activate(dataset)
                        pyautogui.moveTo(dataset['scroll_base'])
                        pyautogui.scroll(-500)
                    time.sleep(float(dataset['speed']))
            # 추후 마이뷰 클릭 or 보드 클릭으로 로직 분개 지점
            else:
                next_step = True

    return next_step


# PROCESS MOUDLES
# 좋아요 클릭 모듈
def select_channel(dataset):
    print('select_channel')
    next_step = False

    win_activate(dataset)
    # dataset['file_name_list'] = ['\heart_empty', '\heart_empty1', '\heart_empty2', '\heart_empty3']
    dataset['file_name_list'] = ['\heart_empty']
    heart_empty = find_location_accuracy(dataset, 0.70)

    dataset['file_name_list'] = ['\heart_full']
    heart_full = find_location_accuracy(dataset, 0.85)

    if len(heart_empty) > 0 or len(heart_full) > 0:
        print("좋아요 찾기 완료 (빈거, 꽉찬거)")
        full_heart = False
        empty_x = 0
        empty_y = 0
        full_x = 0
        full_y = 0

        if len(heart_empty) > 0:
            for loc in heart_empty:
                this_loc = pyautogui.center(loc)
                if (this_loc.y < empty_y or empty_y == 0) and this_loc.x < 450:
                    empty_x = this_loc.x
                    empty_y = this_loc.y

        if len(heart_full) > 0:

            for loc in heart_full:
                this_loc = pyautogui.center(loc)
                if (this_loc.y < full_y or full_y == 0) and this_loc.x < 450:
                    full_x = this_loc.x
                    full_y = this_loc.y

        # 좋아요 클릭된 하트의 값이 좋아요 클릭되지 않은 하트보다 상단에 있을 경우
        # 이미 클릭된 하트로 판단
        # 둘다 존재할 경우
        if len(heart_empty) > 0 and len(heart_full) > 0:
            if full_y == 0:
                full_y = 9999
            if empty_y == 0:
                empty_y = 9999

            if empty_y < full_y:
                curr_loc = (empty_x, empty_y)
            else:
                curr_loc = (full_x, full_y)
                full_heart = True
        elif len(heart_empty) > 0:
            curr_loc = (empty_x, empty_y)
        elif len(heart_full) > 0:
            curr_loc = (full_x, full_y)
            full_heart = True
        print("좋아요 : " + str(full_heart))
        set_time_out = timeout(dataset)
        timeout_flag = False
        capture_flag = False
        while not next_step:
            if check_timeout(set_time_out):
                if not timeout_flag:
                    win_activate(dataset)
                    if not full_heart:
                        print("좋아요 클릭")
                        pyautogui.click(curr_loc)

                    if not capture_flag:
                        dataset['file_name_list'] = ['\capture']
                        capture_icon = find_location(dataset)
                        if len(capture_icon) > 0:
                            capture_loc = pyautogui.center(capture_icon[0])
                            pyautogui.click(capture_loc)
                            time.sleep(float(dataset['speed']))
                            capture_flag = True
                    timeout_flag = True

                time.sleep(float(dataset['speed']))

                # dataset['file_name_list'] = ['\option_dots', '\option_dots1']
                dataset['file_name_list'] = ['\option_dots']
                option_dots = find_location_accuracy(dataset, 0.85)  # 옵션 닷 버튼 찾기
                if len(option_dots) > 0:

                    option_loc_x = 0
                    option_loc_y = 0

                    for loc in option_dots:
                        this_loc = pyautogui.center(loc)
                        if (this_loc.y < option_loc_y or option_loc_y == 0) and this_loc.x < 450:
                            option_loc_x = this_loc.x
                            option_loc_y = this_loc.y

                    title_loc = (option_loc_x, option_loc_y + 30)

                    set_time_out1 = timeout(dataset)
                    timeout_flag1 = False
                    while not next_step:
                        if check_timeout(set_time_out1):
                            if not timeout_flag1:
                                pyautogui.click(title_loc)
                                timeout_flag1 = True

                            while not next_step:

                                # 메인 보드 클릭
                                if is_board(dataset):
                                    next_step = True
                                    print("채널 보드 입장")

                        else:
                            print('채널 보드 입장 불가')
                            set_time_out1 = timeout(dataset)
                            timeout_flag1 = True
            else:
                print('좋아요 클릭 실패')
                set_time_out = timeout(dataset)
                timeout_flag = True
    return next_step


# 보드 클릭 모듈
def click_contents(dataset):
    print('click_contents')
    next_step = False

    # 하단광고 클릭 시 MY VIEW RETURN FLAG 초기화
    dataset['return_my_view'] = False
    # dataset['file_name_list'] = ['\channel_main_option_dots']
    win_activate(dataset)

    while not next_step:

        dataset['file_name_list'] = ['\split_line', '\split_line1']
        channel_split_line = find_location_accuracy(dataset, 0.80)  # 채널 메인 옵션 닷 찾기

        if len(channel_split_line) > 0:
            print('채널 메인 분할 라인 찾음')
            title_x = 0
            title_y = 0
            for loc in channel_split_line:
                this_loc = pyautogui.center(loc)
                if this_loc.x < 450 and this_loc.y > 250:
                    if this_loc.y < title_y or title_y == 0:
                        title_x = this_loc.x
                        title_y = this_loc.y

            if title_x > 0 and title_y > 0:
                title_loc = (title_x - 150, title_y + 50)
                title_loc1 = (title_x - 150, title_y + 100)

                set_time_out = timeout(dataset)
                timeout_flag = False
                while not next_step:
                    if check_timeout(set_time_out):
                        if not timeout_flag:
                            print("채널 보드 클릭!")
                            time.sleep(1)
                            pyautogui.click(title_loc)
                            time.sleep(0.5)
                            pyautogui.click(title_loc1)
                            timeout_flag = True

                        if not is_board(dataset):
                            print('보드 컨텐츠 입장')

                            # 로딩 체크
                            dataset['last_location'] = title_loc
                            next_step = check_loading_capture(dataset)
                    else:
                        set_time_out = timeout(dataset)
                        timeout_flag = False
    return next_step


# 상단 광고 클릭 모듈
def click_top_ad(dataset):
    print('click_top_ad')
    next_step = False
    win_activate(dataset)

    while not next_step:

        # 보드 텍스트 기준 상단광고 위치 찾기
        if is_board(dataset):
            print('상단 광고 찾음')
            dataset['file_name_list'] = ['\main_board_txt']
            board_txt = find_location_accuracy(dataset, 0.75)
            top_ad_x = 0
            top_ad_y = 0
            for loc in board_txt:
                this_loc = pyautogui.center(loc)
                if this_loc.y < 150 or top_ad_y == 0:
                    top_ad_y = this_loc.y
                    top_ad_x = this_loc.x

            top_ad_loc = (top_ad_x, top_ad_y + 70)
            dataset['last_location'] = top_ad_loc
            set_time_out = timeout(dataset)
            timeout_flag = False
            while not next_step:
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        win_activate(dataset)
                        time.sleep(1)
                        pyautogui.click(top_ad_loc)
                        timeout_flag = True
                    # test
                    # time.sleep(float(dataset['loading_wait_time']))
                    print('상단광고 로딩바 로딩 중')
                    next_step = check_loading_capture(dataset)
                    if not next_step:
                        print('상단광고 로딩바 확인 불가')
                else:
                    # pyautogui.click(top_ad_loc)
                    if not next_step:
                        print('상단광고 입장 실패 재시도 클릭')
                        if refresh_reload(dataset):
                            next_step = check_loading_capture(dataset)

                    set_time_out = timeout(dataset)
                    timeout_flag = False
    return next_step


# 하단 광고 클릭 모듈
def click_bottom_ad(dataset):
    print('click_bottom_ad')
    next_step = False
    win_activate(dataset)
    dataset['return_my_view'] = True

    while not next_step:

        # 연관된 주제 보드 찾기
        # dataset['file_name_list'] = ['\similar_msg_txt1', '\similar_msg_txt2', '\similar_msg_txt3']
        dataset['file_name_list'] = ['\similar_msg_txt', '\similar_msg_txt1']
        similar_msg_txt_loc = find_location_accuracy(dataset, 0.80)

        # 이 채널의 다른보드 메시지 찾기
        dataset['file_name_list'] = ['\other_msg_txt', '\more_kakaoview_txt', '\more_kakaoview_txt1']
        other_msg_txt_loc = find_location_accuracy(dataset, 0.80)

        if len(other_msg_txt_loc) == 0 and len(similar_msg_txt_loc) > 0:
            print('하단광고 찾음!')
            bottom_ad_loc = pyautogui.center(similar_msg_txt_loc[0])
            bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 140)
            dataset['last_location'] = bottom_ad_loc
            set_time_out = timeout(dataset)
            timeout_flag = False
            while not next_step:
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        time.sleep(1)
                        pyautogui.click(bottom_ad_loc)
                        timeout_flag = True
                    # test
                    # time.sleep(float(dataset['loading_wait_time']))
                    print('하단광고 로딩바 로딩 중')
                    next_step = check_loading_capture(dataset)
                    if not next_step:
                        print('하단광고 로딩바 확인 불가')
                else:
                    # pyautogui.click(bottom_ad_loc)
                    set_time_out = timeout(dataset)
                    timeout_flag = False
        elif len(other_msg_txt_loc) > 0:
            print('하단광고 찾기 완료!')

            # 하단에 광고가 위치할 수 도 있기에 어느정도를 스크롤한다.
            pyautogui.moveTo(dataset['scroll_base'])
            for i in range(1, 8):
                pyautogui.scroll(-500)
                time.sleep(float(dataset['speed']))

            # 이 채널의 다른보드 메시지 다시 찾기 위에서 스크롤 이동함
            dataset['file_name_list'] = ['\other_msg_txt']
            other_msg_txt_loc = find_location_accuracy(dataset, 0.80)

            dataset['file_name_list'] = ['\more_kakaoview_txt', '\more_kakaoview_txt1']
            more_kakaoview_loc = find_location_accuracy(dataset, 0.75)
            if len(other_msg_txt_loc) > 0:
                bottom_ad_loc = pyautogui.center(other_msg_txt_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y + 400)
            elif len(more_kakaoview_loc) > 0:
                bottom_ad_loc = pyautogui.center(more_kakaoview_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 100)

            dataset['last_location'] = bottom_ad_loc
            set_time_out = timeout(dataset)
            timeout_flag = False
            while not next_step:
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        pyautogui.click(bottom_ad_loc)
                        timeout_flag = True
                    time.sleep(float(dataset['loading_wait_time']))
                    next_step = check_loading_capture(dataset)
                    print('하단광고 로딩 완료')
                else:
                    # pyautogui.click(bottom_ad_loc)
                    if not next_step:
                        print('하단광고 입장 실패 재시도 클릭')
                        if refresh_reload(dataset, bottom_ad_loc):
                            next_step = check_loading_capture(dataset)
                    set_time_out = timeout(dataset)
                    timeout_flag = True
        else:
            print('하단광고 못찾음..')
            win_activate(dataset)
            pyautogui.moveTo(dataset['scroll_base'])
            pyautogui.scroll(-500)
    return next_step


def activate_auto_tour():
    time.sleep(5)

    # 과거 정보
    dataset = {"accuracy": 0.95, "filename_option": "_1", "speed": 0.5, "limit_time": 5, "scroll_speed": 0.5,
               "scroll_count": 5, "mouse_scroll_cnt": 5, "return_my_view": False, "loading_wait_time": 3,
               "win_title": '상민의 Galaxy S20+ 5G',
               "loading_img_list": ['\loading_bar1', '\loading_bar2', '\loading_bar3', '\loading_bar4', '\loading_bar5',
                                    '\loading_bar6', '\loading_bar7', '\loading_bar8', '\loading_bar9'],
               "more_kakao_board": ['\more_kakaoview_txt', '\more_kakaoview_txt1'],
               'file_name_list': ['\home_for_scroll_base', '\home_for_scroll_base1'],
               'loading_msg': False,
               'is_refresh': False}

    home_for_scroll = find_location_accuracy(dataset, 0.75)
    home_for_scroll = pyautogui.center(home_for_scroll[0])
    home_for_scroll = (home_for_scroll.x, home_for_scroll.y - 400)
    dataset['scroll_base'] = home_for_scroll

    # 하트 찾기
    activation = True
    status_cnt = 0
    while activation:
        status_cnt = status_cnt + 1

        # Seq 1 이상부터는 start 모드가 아니다. (my view search 시 영향)
        if status_cnt == 1:
            dataset['start'] = True
        else:
            dataset['start'] = False

        # 메인하트 찾기
        find_heart(dataset)

        # My 뷰 채널 진입
        select_channel(dataset)

        # 채널 컨텐츠 진입
        click_contents(dataset)

        # 상단광고 클릭
        click_top_ad(dataset)

        # 하단광고 클릭
        click_bottom_ad(dataset)


activate_auto_tour()
