import pyautogui
from datetime import datetime, timedelta

import time


def find_location(dataset):
    work_dir = "Z:\HDD1\kakaoview_macro\img"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=float(dataset['accuracy']))
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)

    # print(file_name)
    # print(result)
    return result


def find_location_accuracy(dataset, accuracy):
    work_dir = "Z:\HDD1\kakaoview_macro\img"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=accuracy)
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
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
    next_step = True
    scroll_loc = (18, 931)
    pyautogui.click(scroll_loc)
    time.sleep(float(dataset['speed']))

    dataset['file_name_list'] = ['\scroll_down']
    scroll_down_icon = find_location(dataset)

    if len(scroll_down_icon) > 0:
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
            time.sleep(float(dataset['speed']))
            capture(dataset)
    #else:
        #capture(dataset)
    return next_step


def capture(dataset):
    next_step = False
    return_my_view = dataset['return_my_view']
    dataset['file_name_list'] = ['\capture']
    capture_icon = find_location(dataset)
    if len(capture_icon) > 0:
        capture_loc = pyautogui.center(capture_icon[0])
        pyautogui.click(capture_loc)
        time.sleep(float(dataset['speed']))

        if return_my_view:
            print("마이뷰로 돌아가기")
            dataset['file_name_list'] = ['\my_view_return']
            my_view_return = find_location(dataset)
            if len(my_view_return) > 0:
                my_view_return_loc = pyautogui.center(my_view_return[0])
                pyautogui.click(my_view_return_loc)

                set_time_out = timeout(dataset)
                timeout_flag = False
                while not next_step:
                    if check_timeout(set_time_out):
                        if not timeout_flag:
                            # 2번 클릭 보드 > 채널 > 마이뷰
                            pyautogui.click(my_view_return_loc)
                            time.sleep(float(dataset['speed']))
                            pyautogui.click(my_view_return_loc)
                            timeout_flag = True

                        dataset['file_name_list'] = ['\my_view_text']
                        my_view_text = find_location(dataset)

                        # 메인 보드 클릭
                        if len(my_view_text) > 0:
                            next_step = True
                    else:
                        pyautogui.click(my_view_return_loc)
                        set_time_out = timeout(dataset)
                        timeout_flag = True
        else:
            print("뒤로가기")
            dataset['file_name_list'] = ['\capture_back']
            capture_back = find_location(dataset)
            if len(capture_back) > 0:
                capture_back_loc = pyautogui.center(capture_back[0])
                set_time_out = timeout(dataset)
                timeout_flag = False
                while not next_step:
                    if check_timeout(set_time_out):
                        if not timeout_flag:
                            pyautogui.click(capture_back_loc)
                            timeout_flag = True

                        dataset['file_name_list'] = ['\main_board_txt', '\main_board_txt1', '\main_board_txt2']
                        board_txt = find_location(dataset)

                        # 메인 채널 여부 확인
                        if len(board_txt) > 0:
                            next_step = True
                    else:
                        pyautogui.click(capture_back_loc)
                        set_time_out = timeout(dataset)
                        timeout_flag = True
    return next_step


def check_loading(dataset):
    next_step = False
    print("로딩바 찾기")
    # 로딩바 대기 30초
    set_timeout = datetime.now() + timedelta(seconds=30)

    dataset['file_name_list'] = ['\main_board_txt', '\main_board_txt1', '\main_board_txt2']
    board_txt = find_location(dataset)

    dataset['file_name_list'] = ['\loading_bar1', '\loading_bar2', '\loading_bar3', '\loading_bar4']
    loading_bar = find_location_accuracy(dataset, 0.999)

    # 판단 근거
    # 1. 보드 텍스트가 사라진 것으로 컨텐츠 클릭으로 이동 했다고 판단
    # 2. 로딩바가 보이지 않는 시점이여야 로딩이 완료 되었다고 판단
    if len(board_txt) == 0 and len(loading_bar) == 0:
        print("로딩바 찾음")
        next_step = scroll_down(dataset)
    elif len(loading_bar) > 0:
        loading_finish = False
        while not loading_finish:
            dataset['file_name_list'] = ['\loading_bar1', '\loading_bar2', '\loading_bar3', '\loading_bar4']
            loading_bar = find_location_accuracy(dataset, 0.999)
            if len(loading_bar) > 0:
                loading_finish = True
                next_step = scroll_down(dataset)
            if set_timeout < datetime.now():
                loading_finish = True
    return next_step


def reload(dataset, location):
    print("모듈 반복 재실행")
    dataset['file_name_list'] = ['\capture_back']
    capture_back = find_location(dataset)
    capture_back_loc = pyautogui.center(capture_back[0])
    pyautogui.click(capture_back_loc)
    time.sleep(1)
    pyautogui.click(location)
    return True


def refresh_reload(dataset, location):
    print("리프레시 및 모듈 반복 재실행")

    # BACK BTN
    dataset['file_name_list'] = ['\capture_back']
    capture_back = find_location(dataset)
    capture_back_loc = pyautogui.center(capture_back[0])
    pyautogui.click(capture_back_loc)
    time.sleep(1)

    # 옵션 페이지 리프레시 (광고 변경)
    dataset['file_name_list'] = ['\page_refresh_option']
    board_option = find_location(dataset)
    board_option_loc = pyautogui.center(board_option[0])
    pyautogui.click(board_option_loc)
    time.sleep(0.5)
    dataset['file_name_list'] = ['\page_refresh']
    page_refresh = find_location(dataset)
    page_refresh_loc = pyautogui.center(page_refresh[0])
    pyautogui.click(page_refresh_loc)

    # 보드 재클릭
    pyautogui.click(location)
    return True


def find_next_board_from_view(dataset):
    init = dataset['start']

    dataset['file_name_list'] = ['\setting_icon']
    setting_icon = find_location(dataset)  # 옵션 닷 버튼 찾기
    next_step = False

    if len(setting_icon) > 0:
        if not init:
            while not next_step:
                dataset['file_name_list'] = ['\option_dots', '\option_next_dots', '\option_next_dots1']
                option_dots = find_location(dataset)  # 옵션 닷 버튼 찾기

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
                    pyautogui.moveTo(title_loc)
                    pyautogui.mouseDown()
                    setting_icon_loc = pyautogui.center(setting_icon[0])
                    setting_icon_loc = (setting_icon_loc.x, setting_icon_loc.y + 65)
                    pyautogui.moveTo(setting_icon_loc)
                    pyautogui.mouseUp()
                    next_step = True
                else:
                    print("마이뷰에서 옵션버튼 위치 찾기 실패")
                    pyautogui.moveTo(dataset['scroll_base'])
                    pyautogui.scroll(-500)
                time.sleep(float(dataset['speed']))
        else:
            next_step = True

    return next_step


# PROCESS MOUDLES
# 좋아요 클릭 모듈
def click_myview_heart(dataset):
    next_step = False
    dataset['file_name_list'] = ['\heart_empty', '\heart_empty1', '\heart_empty2', '\heart_empty3']
    heart_empty = find_location(dataset)

    dataset['file_name_list'] = ['\heart_full']
    heart_full = find_location(dataset)

    if len(heart_empty) > 0 or len(heart_full) > 0:
        print("좋아요 찾기 완료 (빈거, 꽉찬거)")
        full_heart = False
        empty_x = 0
        empty_y = 0
        full_x = 0
        full_y = 0
        if len(heart_empty) > 0:
            empty_loc = pyautogui.center(heart_empty[0])
            empty_x = empty_loc.x
            empty_y = empty_loc.y

        if len(heart_full) > 0:
            full_loc = pyautogui.center(heart_full[0])
            full_x = full_loc.x
            full_y = full_loc.y

        # 좋아요 클릭된 하트의 값이 좋아요 클릭되지 않은 하트보다 상단에 있을 경우
        # 이미 클릭된 하트로 판단
        # 둘다 존재할 경우
        if len(heart_empty) > 0 and len(heart_full) > 0:
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

        set_time_out = timeout(dataset)
        timeout_flag = False
        capture_flag = False
        while not next_step:
            if check_timeout(set_time_out):
                if not timeout_flag:
                    if not full_heart:
                        pyautogui.click(curr_loc)

                    if not capture_flag:
                        dataset['file_name_list'] = ['\capture']
                        capture_icon = find_location(dataset)
                        capture_loc = pyautogui.center(capture_icon[0])
                        pyautogui.click(capture_loc)
                        time.sleep(float(dataset['speed']))
                        capture_flag = True
                    timeout_flag = True

                time.sleep(float(dataset['speed']))

                dataset['file_name_list'] = ['\option_dots']
                option_dots = find_location(dataset)  # 옵션 닷 버튼 찾기
                if len(option_dots) > 0:
                    title_loc = pyautogui.center(option_dots[0])
                    title_loc = (title_loc.x, title_loc.y + 30)

                    set_time_out1 = timeout(dataset)
                    timeout_flag1 = False
                    while not next_step:
                        if check_timeout(set_time_out1):
                            if not timeout_flag1:
                                pyautogui.click(title_loc)
                                timeout_flag1 = True

                            dataset['file_name_list'] = ['\main_board_txt', '\main_board_txt1', '\main_board_txt2']
                            board_txt = find_location(dataset)

                            # 메인 보드 클릭
                            if len(board_txt) > 0:
                                print("메인보드 클릭")
                                next_step = click_board(dataset)

                        else:
                            print('메인보드 인식 불가 마이뷰-> 메인보드 클릭 재시도')
                            pyautogui.click(curr_loc)
                            set_time_out1 = timeout(dataset)
                            timeout_flag1 = True
            else:
                print('좋아요 클릭 실패 (좋아오 클릭된 상태를 못찾음)')
                if not full_heart:
                    pyautogui.click(curr_loc)
                set_time_out = timeout(dataset)
                timeout_flag = True

    return next_step


# 보드 클릭 모듈
def click_board(dataset):
    next_step = False

    # 하단광고 클릭 시 MY VIEW RETURN FLAG 초기화
    dataset['return_my_view'] = False
    # dataset['file_name_list'] = ['\channel_main_option_dots']
    dataset['file_name_list'] = ['\split_line']
    chan_main_op_dots = find_location(dataset)  # 채널 메인 옵션 닷 찾기
    if len(chan_main_op_dots) > 0:
        print('채널 메인에 옵션 버튼 찾음')
        title_loc = pyautogui.center(chan_main_op_dots[0])
        title_loc = (title_loc.x - 150, title_loc.y + 50)

        set_time_out = timeout(dataset)
        timeout_flag = False
        while not next_step:
            if check_timeout(set_time_out):
                if not timeout_flag:
                    pyautogui.click(title_loc)
                    timeout_flag = True
                time.sleep(float(dataset['loading_wait_time']))
                next_step = check_loading(dataset)
                if next_step:
                    print('로딩바 체크완료 메인보드 로딩 끝')
            else:
                if next_step:
                    print('채널 메인보드 확인 불가 재실행')
                    if reload(dataset, title_loc):
                        next_step = check_loading(dataset)

                set_time_out = timeout(dataset)
                timeout_flag = True
    return next_step


# 상단 광고 클릭 모듈
def click_top_ad(dataset):
    next_step = False
    dataset['file_name_list'] = ['\main_board_txt', '\main_board_txt1', '\main_board_txt2']
    board_txt = find_location(dataset)

    # 보드 텍스트 기준 상단광고 위치 찾기
    if len(board_txt) > 0:
        print('상단 광고 찾음')
        top_ad_loc = pyautogui.center(board_txt[0])
        top_ad_loc = (top_ad_loc.x, top_ad_loc.y + 70)

        set_time_out = timeout(dataset)
        timeout_flag = False
        while not next_step:
            if check_timeout(set_time_out):
                if not timeout_flag:
                    pyautogui.click(top_ad_loc)
                    timeout_flag = True
                time.sleep(float(dataset['loading_wait_time']))
                print('상단광고 로딩바 로딩 중')
                next_step = check_loading(dataset)
                if not next_step:
                    print('상단광고 로딩바 확인 불가')
            else:
                # pyautogui.click(top_ad_loc)
                if not next_step:
                    print('상단광고 입장 실패 재시도 클릭')
                    if refresh_reload(dataset, top_ad_loc):
                        next_step = check_loading(dataset)

                set_time_out = timeout(dataset)
                timeout_flag = True
    return next_step


# 하단 광고 클릭 모듈
def click_bottom_ad(dataset):
    next_step = False
    dataset['return_my_view'] = True

    while not next_step:

        # 연관된 주제 보드 찾기
        dataset['file_name_list'] = ['\similar_msg_txt1', '\similar_msg_txt2', '\similar_msg_txt3']
        similar_msg_txt_loc = find_location(dataset)

        # 이 채널의 다른보드 메시지 찾기
        dataset['file_name_list'] = ['\other_msg_txt', '\more_kakaoview_txt']
        other_msg_txt_loc = find_location(dataset)

        if len(other_msg_txt_loc) == 0 and len(similar_msg_txt_loc) > 0:
            print('하단광고 찾음!')
            bottom_ad_loc = pyautogui.center(similar_msg_txt_loc[0])
            bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 140)

            set_time_out = timeout(dataset)
            timeout_flag = False
            while not next_step:
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        pyautogui.click(bottom_ad_loc)
                        timeout_flag = True
                    time.sleep(float(dataset['loading_wait_time']))
                    print('하단광고 로딩바 로딩 중')
                    next_step = check_loading(dataset)
                    if not next_step:
                        print('하단광고 로딩바 확인 불가')
                else:
                    # pyautogui.click(bottom_ad_loc)
                    if not next_step:
                        print('하단광고 입장 실패 재시도 클릭')
                        if refresh_reload(dataset, bottom_ad_loc):
                            next_step = check_loading(dataset)
                    set_time_out = timeout(dataset)
                    timeout_flag = True
        elif len(other_msg_txt_loc) > 0:
            print('하단광고 찾기 완료!')

            # 하단에 광고가 위치할 수 도 있기에 어느정도를 스크롤한다.
            for i in range(1, 5):
                pyautogui.moveTo(dataset['scroll_base'])
                pyautogui.scroll(-500)
                time.sleep(float(dataset['speed']))

            # 이 채널의 다른보드 메시지 다시 찾기 위에서 스크롤 이동함
            dataset['file_name_list'] = ['\other_msg_txt']
            other_msg_txt_loc = find_location(dataset)
            dataset['file_name_list'] = ['\more_kakaoview_txt']
            more_kakaoview_loc = find_location(dataset)
            if len(other_msg_txt_loc) > 0:
                bottom_ad_loc = pyautogui.center(other_msg_txt_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y + 400)
            else:
                bottom_ad_loc = pyautogui.center(more_kakaoview_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 100)

            set_time_out = timeout(dataset)
            timeout_flag = False
            while not next_step:
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        pyautogui.click(bottom_ad_loc)
                        timeout_flag = True
                    time.sleep(float(dataset['loading_wait_time']))
                    next_step = check_loading(dataset)
                    print('하단광고 로딩 완료')
                else:
                    # pyautogui.click(bottom_ad_loc)
                    if not next_step:
                        print('하단광고 입장 실패 재시도 클릭')
                        if refresh_reload(dataset, bottom_ad_loc):
                            next_step = check_loading(dataset)
                    set_time_out = timeout(dataset)
                    timeout_flag = True
        else:
            print('하단광고 못찾음..')
            pyautogui.moveTo(dataset['scroll_base'])
            pyautogui.scroll(-500)
    return next_step


def activate_auto_tour():

    # WINDOW ACTIVATE
    window = pyautogui.getWindowsWithTitle('상민의 Galaxy S20+ 5G')[0]
    window.activate()

    # 과거 정보
    dataset = {"accuracy": 0.80,
               "filename_option": "_1",
               "speed": 0.5,
               "limit_time": 5,
               "scroll_speed": 0.5,
               "scroll_count": 3,
               "mouse_scroll_cnt": 5,
               "return_my_view": False,
               "loading_wait_time": 3,
               "my_window":window
               }

    dataset['file_name_list'] = ['\home_for_scroll_base', '\home_for_scroll_base1']
    home_for_scroll = find_location(dataset)
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
        next_step = False
        while not next_step:
            board_step = False
            while not board_step:
                if find_next_board_from_view(dataset):
                    myview_heart_step = False
                    while not myview_heart_step:
                        if click_myview_heart(dataset):
                            top_ad_step = False
                            while not top_ad_step:
                                if click_top_ad(dataset):
                                    bottom_ad_step = False
                                    while not bottom_ad_step:
                                        next_step = click_bottom_ad(dataset)
                                        bottom_ad_step = next_step
                                        top_ad_step = next_step
                                        myview_heart_step = next_step
                                        board_step = next_step


activate_auto_tour()
