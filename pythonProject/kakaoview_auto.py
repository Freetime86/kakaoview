import pyautogui
from datetime import datetime, timedelta
from PIL import ImageGrab
import os
import time
import sys

#시스템 설정
pyautogui.FAILSAFE = False

def reservation_starter(dataset):
    is_start_time = False

    scroll_loc = (15, 953)
    pyautogui.click(scroll_loc)
    time.sleep(float(dataset['speed']))

    dataset['file_name_list'] = ['\scroll_up']
    scroll_up_icon = find_location(dataset)

    while not is_start_time:
        now = datetime.now()
        current_time = now.strftime("%Y%m%d%H%M")
        print(str(datetime.now().strftime("%X")) + " : " + current_time)
        if int(current_time) >= int(dataset['reservation']):
            is_start_time = True

            dataset['file_name_list'] = ['\scroll_close']
            scroll_close = find_location_accuracy(dataset, 0.80)
            if len(scroll_close) > 0:
                scroll_close_loc = pyautogui.center(scroll_close[0])
            pyautogui.moveTo(scroll_close_loc)
            pyautogui.mouseDown()
            pyautogui.moveTo(5, scroll_close_loc.y)
            pyautogui.mouseUp()
            print(str(datetime.now().strftime("%X")) + " : " + "매크로 시작")
        else:
            if len(scroll_up_icon) > 0:
                scroll_up_loc = pyautogui.center(scroll_up_icon[0])
                pyautogui.click(scroll_up_loc)
                print(str(datetime.now().strftime("%X")) + " : " + "예약 시간 대기 중")
        time.sleep(5)


def win_activate(dataset):
    for title in dataset['win_title']:
        win_element = pyautogui.getWindowsWithTitle(title)
        if len(win_element) > 0:
            window = win_element[0]
            window.activate()
            break


def mobile_device():
    work_dir = os.getcwd() + "\img"
    file_ext = ".png"
    galaxy_s20plus = ['\s20plus_b1', '\s20plus_w1', '\s20plus_b2', '\s20plus_w2']
    galaxy_s20 = ['\s20_w1']

    result = ""
    for file_name in galaxy_s20plus:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + file_ext, confidence=0.80)
        out_list = list(out_list)
        if len(out_list) > 0:
            result = result + "\s20plus"
            break
    for file_name in galaxy_s20:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + file_ext, confidence=0.80)
        out_list = list(out_list)
        if len(out_list) > 0:
            result = result + "\s20plus"
            break
    return result


def option_figure(dataset):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
    file_ext = ".png"
    file_option_1 = ['\setting_icon_1', '\setting_icon1_1']
    file_option_2 = ['\setting_icon_2', '\setting_icon1_2']

    result = ""
    for file_name in file_option_1:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + file_ext, confidence=0.80)
        out_list = list(out_list)
        if len(out_list) > 0:
            result = "_1"
            break
    for file_name in file_option_2:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + file_ext, confidence=0.80)
        out_list = list(out_list)
        if len(out_list) > 0:
            result = "_2"
            break
    return result


def getPixel():
    screen = ImageGrab.grab()
    location = (410, 980)
    color = screen.getpixel(location)

    return color


def check_pixel_load(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "PAGE 로드 체크 시작")
    screen = ImageGrab.grab()
    set_x = 0
    set_y = 0
    location = (set_y, set_x)
    pos_color = screen.getpixel(location)
    result = False
    init = True
    for index in range(0, 9):
        if set_x < 300:
            set_x = set_x + 100
        elif set_x >= 300:
            set_x = 100

        if index % 3 == 0:
            set_y = set_y + 300
        location = (set_y, set_x)

        if init:
            pos_color = screen.getpixel(location)
            print(str(datetime.now().strftime("%X")) + " : " + "로드 체크 프로세스 최초 레코드 : " + str(pos_color))
            init = False
        else:
            color = screen.getpixel(location)
            print(str(datetime.now().strftime("%X")) + " : " + "로드 체크 :::: " + str(pos_color) + "  |  " + str(color))
            if color != pos_color:
                result = True
                print(str(datetime.now().strftime("%X")) + " : " + "청상 페이지 확인 :::: " + str(pos_color) + "  |  " + str(color))
                break
    return result


def find_dynamic_pop(dataset, accuracy):
    work_dir = os.getcwd() + "\img\popup"
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + file_ext,
                                               confidence=accuracy)
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def find_location(dataset):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
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
    return result


def find_location_accuracy(dataset, accuracy):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
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


def find_sel_region_accuracy(dataset, accuracy, xx, xy, yx, yy):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=accuracy, region=(xx, xy, yx, yy))
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def find_location_detail(dataset, accuracy, xx, xy, yx, yy):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        # print(str(datetime.now().strftime("%X")) + " : " + "find_location : " + file_name + dataset['filename_option'] + file_ext)
        out_list = pyautogui.locateAllOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                               confidence=accuracy, region=(xx, xy, yx, yy))
        out_list = list(out_list)
        if len(out_list) > 0:
            for data in out_list:
                result.append(data)
    return result


def find_loading_status(dataset, accuracy):
    work_dir = os.getcwd() + "\img" + dataset['mobile_type']
    file_ext = ".png"
    file_name_list = dataset['file_name_list']
    result = []
    for file_name in file_name_list:
        print(str(datetime.now().strftime("%X")) + " : " + "find_location : " + file_name + dataset['filename_option'] + file_ext)
        out_loc = pyautogui.locateOnScreen(work_dir + file_name + dataset['filename_option'] + file_ext,
                                           confidence=accuracy, region=(5, 100, 446, 125))
        result.append(out_loc)
    return result


def is_board(dataset):
    result = False
    dataset['file_name_list'] = ['\main_board_txt']
    board_loc = find_location_accuracy(dataset, 0.75)

    if len(board_loc) > 0:
        result = True
    #dataset['file_name_list'] = ['\channel_main_option_dots']
    #board_option_dots = find_location_accuracy(dataset, 0.80)

    #result = False
    #for loc in board_txt:
    #    this_loc = pyautogui.center(loc)
    #    if this_loc.y < 120:
    #        for option_loc in board_option_dots:
    #            op_loc = pyautogui.center(option_loc)
    #            if 210 < op_loc.y < 270:
    #                result = True
    return result


def is_my_view(dataset):
    result = False
    dataset['file_name_list'] = ['\my_view_text']
    my_view_text = find_location_detail(dataset, 0.70, 10, 80, 50, 120)
    if len(my_view_text) > 0:
        result = True
    return result


def is_view(dataset):
    dataset['file_name_list'] = ['\view_check']
    board_txt = find_location_accuracy(dataset, 0.70)

    dataset['file_name_list'] = ['\channel_main_option_dots']
    board_option_dots = find_location_accuracy(dataset, 0.70)

    result = False
    for loc in board_txt:
        this_loc = pyautogui.center(loc)
        if this_loc.y < 120:
            for option_loc in board_option_dots:
                op_loc = pyautogui.center(option_loc)
                if 210 < op_loc.y < 270:
                    result = True
    return result


def is_loaded(dataset):
    result = True


    set_time_out = datetime.now() + timedelta(seconds=30)

    next_step = False
    init = True
    print(str(datetime.now().strftime("%X")) + " : " + "페이지 로드, SCROLL DOWN")
    scroll_down(dataset)
    while not next_step:
        if check_timeout(set_time_out):

            screen = ImageGrab.grab()
            set_x = 4
            set_y = 126
            location = (set_x, set_y)
            color = screen.getpixel(location)
            # YELLOW BAR 판단
            if color[0] > 220 and color[1] > 200 and color[2] < 150:
                next_step = False
            elif color[0] > 190 and color[1] > 170 and color[2] < 50:
                next_step = False
            else:
                next_step = True

            # y = 125 try
            if result and next_step:
                set_y = set_y - 1
                location = (set_x, set_y)
                color = screen.getpixel(location)
                # YELLOW BAR 판단
                if color[0] > 220 and color[1] > 200 and color[2] < 150:
                    next_step = False
                elif color[0] > 190 and color[1] > 170 and color[2] < 50:
                    next_step = False
                else:
                    next_step = True

            # y = 124 try
            if result and next_step:
                set_y = set_y - 1
                location = (set_x, set_y)
                color = screen.getpixel(location)
                # YELLOW BAR 판단
                if color[0] > 220 and color[1] > 200 and color[2] < 150:
                    next_step = False
                elif color[0] > 190 and color[1] > 170 and color[2] < 50:
                    next_step = False
                else:
                    next_step = True

            # y = 123 try
            if result and next_step:
                set_y = set_y - 1
                location = (set_x, set_y)
                color = screen.getpixel(location)
                # YELLOW BAR 판단
                if color[0] > 220 and color[1] > 200 and color[2] < 150:
                    next_step = False
                elif color[0] > 190 and color[1] > 170 and color[2] < 50:
                    next_step = False
                else:
                    next_step = True

            if init and not next_step:
                print(str(datetime.now().strftime("%X")) + " : " + "페이지 로딩 중...")
                init = False

        else:
            print(str(datetime.now().strftime("%X")) + " : " + "페이지 로딩 TIMEOUT!! 재처리 시작")
            result = False
            next_step = True

    return result


def timeout(dataset):
    timeout = datetime.now() + timedelta(seconds=float(dataset['limit_time']))
    return timeout


def check_timeout(timeout):
    result = True
    if timeout < datetime.now():
        result = False
        print(str(datetime.now().strftime("%X")) + " : " + "TIME OUT! RETRY!")
    return result


def dynamic_action(dataset):
    result = True
    dataset['file_name_list'] = ['\channel_add']
    # 채널 추가 변수 삭제
    channel_add = find_location_accuracy(dataset, 0.70)
    if len(channel_add) > 0:
        action_back(dataset)

    dataset['file_name_list'] = ['\connecting_msg']
    # 다른프로그램 연결 광고
    connecting_msg = find_location_accuracy(dataset, 0.70)
    if len(connecting_msg) > 0:
        action_back(dataset)
        result = False

    dataset['file_name_list'] = ['\certificate']
    # 카카오뱅크 본인인증
    certificate = find_location_accuracy(dataset, 0.70)
    if len(certificate) > 0:
        dataset['pop_target'] = (225, 656)
        pop_close(dataset, 1)
        # action_back(dataset)
        result = False

    # 팝업 제거 실시간 추가
    # 뷰티영APP
    dataset['file_name_list'] = ['\pop1']
    dataset['pop_target'] = (384, 264)
    pop_close(dataset, 1)

    # AKIII CLASSIC 카카오톡 채널친구 팝업
    dataset['file_name_list'] = ['\pop2']
    dataset['pop_target'] = (413, 843)
    pop_close(dataset, 1)

    # 인증서 선택
    dataset['file_name_list'] = ['\pop3']
    dataset['pop_target'] = (129, 934)
    pop_close(dataset, 1)

    # 지금 이페이지를 나가면
    dataset['file_name_list'] = ['\pop4']
    dataset['pop_target'] = (394, 656)
    pop_close(dataset, 1)

    # 아우디 보안 경고
    dataset['file_name_list'] = ['\pop5']
    dataset['pop_target'] = (300, 574)
    pop_close(dataset, 3)
    dataset['file_name_list'] = ['\pop8']
    dataset['pop_target'] = (300, 574)
    pop_close(dataset, 3)

    # 이벤트
    dataset['file_name_list'] = ['\pop6']
    dataset['pop_target'] = (416, 464)
    # pop_close(dataset, 1)

    # GPS 허용안함
    dataset['file_name_list'] = ['\pop7']
    dataset['pop_target'] = (255, 933)
    pop_close(dataset, 1)

    # 카카오뱅크 본인인증
    # dataset['file_name_list'] = ['\pop9']
    # dataset['pop_target'] = (345, 1018)
    # pop_close(dataset, 2)

    # 화장품 광고
    dataset['file_name_list'] = ['\pop10']
    dataset['pop_target'] = (134, 901)
    pop_close(dataset, 2)

    # 부동산 광고
    dataset['file_name_list'] = ['\pop11']
    dataset['pop_target'] = (418, 336)
    pop_close(dataset, 1)

    # 옷 앱 팝업 제거
    dataset['file_name_list'] = ['\pop12']
    dataset['pop_target'] = (390, 356)
    pop_close(dataset, 1)

    # 향수광고
    dataset['file_name_list'] = ['\pop13']
    dataset['pop_target'] = (338, 724)
    pop_close(dataset, 1)

    # 위치기반 GPS 메시지
    dataset['file_name_list'] = ['\pop14']
    dataset['pop_target'] = (299, 567)
    pop_close(dataset, 1)

    # 한샘광고
    dataset['file_name_list'] = ['\pop15']
    dataset['pop_target'] = (223, 952)
    pop_close(dataset, 1)

    # AKIII CLASSIC 앱구매 팝업
    dataset['file_name_list'] = ['\pop16']
    dataset['pop_target'] = (413, 652)
    pop_close(dataset, 1)

    # 광고 구글플레이 팝업 제거
    dataset['file_name_list'] = ['\pop17']
    dataset['pop_target'] = (417, 418)
    pop_close(dataset, 1)

    # GPS 사용 여부 차단 black
    dataset['file_name_list'] = ['\pop18']
    dataset['pop_target'] = (375, 566)
    pop_close(dataset, 1)

    # 캐주얼 옷 앱 구매시 할인 팝업
    dataset['file_name_list'] = ['\pop19']
    dataset['pop_target'] = (390, 780)
    pop_close(dataset, 1)

    # 캐주얼 옷 앱 구매시 할인 팝업
    dataset['file_name_list'] = ['\pop20']
    dataset['pop_target'] = (227, 765)
    dataset['pop_target'] = (391, 761)
    pop_close(dataset, 1)

    # gs 프레시몰
    dataset['file_name_list'] = ['\pop21']
    dataset['pop_target'] = (225, 691)
    pop_close(dataset, 1)

    # 쿠키 수집에 대한 동의
    dataset['file_name_list'] = ['\pop22']
    dataset['pop_target'] = (130, 870)
    pop_close(dataset, 1)

    # 위치기반 동의 차단
    dataset['file_name_list'] = ['\pop23']
    dataset['pop_target'] = (300, 569)
    pop_close(dataset, 1)

    # GPS 사용 여부 차단 white
    dataset['file_name_list'] = ['\pop24']
    dataset['pop_target'] = (375, 566)
    pop_close(dataset, 1)

    return result


def pop_close(dataset, cnt):
    # 다른프로그램 연결 광고
    pop1 = find_dynamic_pop(dataset, 0.80)
    if len(pop1) > 0:
        for i in range(0, cnt):
            pyautogui.click(dataset['pop_target'])
            time.sleep(1)


def action_back(dataset):
    dataset['file_name_list'] = ['\capture_back', '\capture_back1']
    capture_back = find_sel_region_accuracy(dataset, 0.7, 20, 980, 440, 1030)
    if len(capture_back) > 0:
        capture_back_loc = pyautogui.center(capture_back[0])
        pyautogui.click(capture_back_loc)


def scroll_down(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "스크롤 실행 모듈 시작")
    
    if not is_board(dataset):
        dataset['file_name_list'] = ['\scroll_close']
        scroll_close = find_location_accuracy(dataset, 0.70)
        scroll_loc = (18, 980)

        if len(scroll_close) == 0:
            pyautogui.click(scroll_loc)
        print(str(datetime.now().strftime("%X")) + " : " + "스크롤 APP ON!")
        time.sleep(float(dataset['speed']))
    
        if dataset['is_refresh']:
            pyautogui.click(scroll_loc)
            dataset['is_refresh'] = False
    
        dataset['file_name_list'] = ['\scroll_down']
        scroll_down_icon = find_location(dataset)
        if len(scroll_down_icon) > 0:
            scroll_down_loc = pyautogui.center(scroll_down_icon[0])
    
            for i in range(0, 2):
                pyautogui.click(scroll_down_loc)
    else:
        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치는 메인 채널. 모듈 재 실행")
    return


def capture_module(dataset):
    result = False
    dataset['file_name_list'] = ['\capture', '\capture1']
    capture_icon = find_location_accuracy(dataset, 0.70)
    if len(capture_icon) > 0:
        capture_loc = pyautogui.center(capture_icon[0])
        pyautogui.click(capture_loc)
        time.sleep(1)
        result = True
    return result


# 캡처 후 이전 process 로 복귀
def capture_back(dataset):

    result = False
    print(str(datetime.now().strftime("%X")) + " : " + "캡처 모듈 실행")

    dataset['file_name_list'] = ['\scroll_down']
    scroll_down_icon = find_location(dataset)

    if len(scroll_down_icon) > 0:
        scroll_down_loc = pyautogui.center(scroll_down_icon[0])
    else:
        print(str(datetime.now().strftime("%X")) + " : " + "SCROLL APP 이 확인 되지 않음, SCROLL APP ON!")
        scroll_loc = (18, 980)
        pyautogui.click(scroll_loc)
        return

    dataset['file_name_list'] = ['\capture', '\capture1']
    capture_icon = find_location_accuracy(dataset, 0.70)

    if len(capture_icon) > 0:

        if not is_board(dataset) and not is_my_view(dataset):

            print(str(datetime.now().strftime("%X")) + " : " + "다이나믹 필터 처리 중...")
            if dynamic_action(dataset):
                print(str(datetime.now().strftime("%X")) + " : " + "다이나믹 필터 처리 완료")

                #print(str(datetime.now().strftime("%X")) + " : " + "페이지 2차 SCROLL DOWN")
                #pyautogui.click(scroll_down_loc)
                #time.sleep(1)
                
                #로딩 한번 더 체크
                if is_loaded(dataset):
                    print(str(datetime.now().strftime("%X")) + " : " + "페이지 로드 2차 확인 완료")
                    capture_loc = pyautogui.center(capture_icon[0])

                    dataset['file_name_list'] = ['\scroll_close']
                    scroll_close = find_location_accuracy(dataset, 0.80)
                    time.sleep(1)

                    # 스크롤 숨기기
                    if len(scroll_close) > 0:
                        scroll_close_loc = pyautogui.center(scroll_close[0])
                        pyautogui.moveTo(scroll_close_loc)
                        pyautogui.mouseDown()
                        pyautogui.moveTo(5, scroll_close_loc.y)
                        pyautogui.mouseUp()
                        print(str(datetime.now().strftime("%X")) + " : " + "SCROLL APP 비활성화")

                        if not is_board(dataset):
                            pyautogui.click(capture_loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "화면 이미지 캡처")
                            time.sleep(1)
                            result = True
                        else:
                            print(str(datetime.now().strftime("%X")) + " : " + "캡처 위치가 보드 입니다.")
                            refresh_reload(dataset)
                    else:
                        print(str(datetime.now().strftime("%X")) + " : " + "스크롤 APP 확인 불가, 캡처 그대로 진행")
                        if not is_board(dataset):
                            pyautogui.click(capture_loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "화면 이미지 캡처")
                            time.sleep(1)
                            result = True
                        else:
                            print(str(datetime.now().strftime("%X")) + " : " + "캡처 위치가 보드 입니다.")
                            print(str(datetime.now().strftime("%X")) + " : " + "마지막 액션 재 실행.")
                            pyautogui.click(dataset['last_location'])
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "페이지 로드 정상적인 판단 불가, 모듈 재 실행")
                    refresh_reload(dataset)
            else:
                print(str(datetime.now().strftime("%X")) + " : " + "다이나믹 필터 후처리 모듈 실행")
                refresh(dataset)
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치가 보드 또는 마이뷰에 있어서 캡처가 불가능 합니다.")
    else:
        print(str(datetime.now().strftime("%X")) + " : " + "캡처 버튼을 찾을 수가 없습니다.")
    return result


def back_to_home(dataset):
    result = False
    print(str(datetime.now().strftime("%X")) + " : " + "EXIT 모듈 실행")
    if dataset['return_my_view']:
        print(str(datetime.now().strftime("%X")) + " : " + "마이뷰 이동 모듈 실행")
        dataset['file_name_list'] = ['\capture_back', '\capture_back1']
        my_view_return = find_sel_region_accuracy(dataset, 0.7, 20, 980, 440, 1030)

        if len(my_view_return) > 0:

            my_view_return_loc = pyautogui.center(my_view_return[0])
            timeout_flag = False
            first_try = True
            try_count = 0
            pos_screen = (0, 0)
            set_time_out = datetime.now() + timedelta(seconds=10)
            next_step = False
            while not next_step:
                curr_screen = getPixel()
                if check_timeout(set_time_out):
                    if not timeout_flag:

                        dataset['file_name_list'] = ['\win_close', '\win_close1']
                        win_close = find_sel_region_accuracy(dataset, 0.8, 5, 70, 440, 150)

                        if len(win_close) > 0 and try_count == 0:
                            win_close_Loc = pyautogui.center(win_close[0])
                            pyautogui.click(win_close_Loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "X 버튼 클릭 탈출 시도")
                            try_count = try_count + 1
                            time.sleep(1)
                        else:
                            if try_count > 3 and curr_screen == pos_screen:
                                if not is_board(dataset):
                                    pyautogui.click(my_view_return_loc)
                                    print(str(datetime.now().strftime("%X")) + " : " + "뒤로가기 더블 클릭")
                                pyautogui.click(my_view_return_loc)
                                try_count = 0
                            else:
                                pos_screen = getPixel()
                                if first_try:
                                    pyautogui.click(my_view_return_loc)
                                    print(str(datetime.now().strftime("%X")) + " : " + "마이뷰 이동 전처리")
                                    first_try = False
                                    time.sleep(1)
                                else:
                                    pyautogui.click(my_view_return_loc)
                                    print(str(datetime.now().strftime("%X")) + " : " + "마이뷰 이동")
                                    try_count = try_count + 1
                            timeout_flag = True

                    # 마이뷰 복귀 확인
                    if is_my_view(dataset):
                        print(str(datetime.now().strftime("%X")) + " : " + "마이뷰 돌아가기 완료")
                        next_step = True
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "마이뷰를 찾을 수 없습니다.")
                    timeout_flag = False
                    set_time_out = timeout(dataset)


    else:
        print(str(datetime.now().strftime("%X")) + " : " + "뒤로 가기 모듈 실행")
        dataset['file_name_list'] = ['\capture_back', '\capture_back1']
        capture_back = find_sel_region_accuracy(dataset, 0.7, 20, 980, 440, 1030)

        if is_board(dataset):
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치는 내 채널 메인에 있습니다.")
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치에서 내 채널 메인을 식별할 수 없습니다.")
        if len(capture_back) > 0 and not is_board(dataset):

            capture_back_loc = pyautogui.center(capture_back[0])
            set_time_out = timeout(dataset)
            timeout_flag = False
            next_step = False
            try_count = 0
            pos_screen = (0, 0)
            while not next_step:
                curr_screen = getPixel()
                if check_timeout(set_time_out):
                    if not timeout_flag:
                        dataset['file_name_list'] = ['\win_close', '\win_close1']
                        win_close = find_sel_region_accuracy(dataset, 0.8, 5, 70, 440, 150)

                        cancel = False
                        if len(win_close) > 0:
                            cancel = True
                        if try_count > 5 and curr_screen == pos_screen or cancel:
                            if len(win_close) > 0 and try_count > 5:
                                if not is_board(dataset):
                                    win_close_Loc = pyautogui.center(win_close[0])
                                    pyautogui.click(win_close_Loc)
                                    print(str(datetime.now().strftime("%X")) + " : " + "X 버튼을 이용하여 탈출 추가 프로세스를 실행")
                                    try_count = 0
                            else:
                                if not is_my_view(dataset):
                                    if not is_board(dataset):
                                        if try_count > 5:
                                            print(str(datetime.now().strftime("%X")) + " : " + "5회 시도 : 보드 인식 불가, 연타로 빠져나가기 시도")
                                            pyautogui.click(capture_back_loc)
                                            try_count = 0
                                            print(str(datetime.now().strftime("%X")) + " : " + "탈출 시도 횟수 : " + str(try_count))
                                            print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 1 실행 : CLEAR")
                                        pyautogui.click(capture_back_loc)
                                        print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 2 실행 : CLEAR")
                                        try_count = try_count + 1
                                else:
                                    pyautogui.click(dataset['my_channel'])
                                    print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, 마지막 보드 재 진입")


                        else:
                            if not is_board(dataset):
                                if not is_my_view(dataset):
                                    print(str(datetime.now().strftime("%X")) + " : " + "보드로 돌아갈 수 없음. 프로그램 재 기동")
                                    pyautogui.click(capture_back_loc)
                                    try_count = try_count + 1
                                else:
                                    print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, BACK BTN 사용 불가")
                                    if dataset['my_channel'] is not None:
                                        pyautogui.click(dataset['my_channel'])
                                        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, 마지막 보드 재 진입")

                        pos_screen = getPixel()
                        timeout_flag = True

                    # 메인 채널 여부 확인
                    if is_board(dataset):
                        next_step = True
                else:
                    timeout_flag = False
                    set_time_out = timeout(dataset)

    return next_step


def check_loading_capture(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "PAGE LOADING.....")
    # 광고 로딩 후 나가리 되는 광고들 존재
    time.sleep(2)
    next_step = False

    # 다이나믹 액션으로 쓰레기 제거
    # dynamic_action(dataset)

    # 로딩바 대기 30초
    set_timeout = datetime.now() + timedelta(seconds=10)

    # 판단 근거
    # 1. 보드 텍스트가 사라진 것으로 컨텐츠 클릭으로 이동 했다고 판단
    # 2. 로딩바가 보이지 않는 시점이여야 로딩이 완료 되었다고 판단

    while not next_step:

        # 현재 위치가 보드가 아님을 판단
        if not is_board(dataset):

            # 보드 로딩바 확인 불가 (입장 완료 또는 입장 실패) 확인 될 때까지 재실행
            loading_finish = False
            while not loading_finish:
                loading_finish = True
                next_step = scroll_down(dataset)

                # 일정 시간 후에도 기능이 동작하지 않으면 timeout (refresh)
                if not loading_finish:
                    if set_timeout < datetime.now():
                        print(str(datetime.now().strftime("%X")) + " : " + "LOADING TIMEOUT : FAIL")
                        refresh_reload(dataset)

                        # 로딩바 대기 30초
                        set_timeout = datetime.now() + timedelta(seconds=30)
        else:
            # 일정 시간 후에도 기능이 동작하지 않으면 timeout (refresh)
            if set_timeout < datetime.now():
                print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 채널 동작 없음: FAIL")
                connecting_msg = find_location_accuracy(dataset, 0.80)
                if len(connecting_msg) > 0:
                    print(str(datetime.now().strftime("%X")) + " : " + "연결프로그램 메시지 재 갱신만 진행 : CLEAR")
                if is_board(dataset) or len(connecting_msg) > 0:
                    refresh(dataset)
                else:
                    refresh_reload(dataset)

                # 로딩바 대기 30초
                set_timeout = datetime.now() + timedelta(seconds=30)

    return next_step


def refresh(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + '재 갱신 모듈 실행')

    next_step = False
    # main channel check
    channel_main_flag = False
    try_count = 0
    pos_screen = (0, 0)

    while not next_step:
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
                    page_refresh_loc = pyautogui.center(page_refresh[0])
                    pyautogui.click(page_refresh_loc)
                    print(str(datetime.now().strftime("%X")) + " : " + "새로고침 실행 : CLEAR")
                    page_refresh_flag = True
                    dataset['is_refresh'] = True
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "새로고침 옵션 확인 불가 : FAIL")
                    if is_board(dataset):
                        pyautogui.doubleClick(board_option_loc)
                        time.sleep(0.5)

            # 보드 재클릭
            time.sleep(1)
            pyautogui.click(dataset['last_location'])

            next_step = True

    return next_step


def refresh_reload(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "재 기동 실행 : CLEAR")

    next_step = False
    # main channel check
    channel_main_flag = False
    try_count = 0
    pos_screen = (0, 0)

    # 선처리 다이나믹 변수 처리
    dynamic_action(dataset)

    while not channel_main_flag:
        if not is_board(dataset):

            curr_screen = getPixel()

            # BACK BTN
            dataset['file_name_list'] = ['\capture_back', '\capture_back1']
            capture_back = find_sel_region_accuracy(dataset, 0.7, 20, 980, 440, 1030)

            if len(capture_back) > 0:
                print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 위치 확인 : CLEAR")
                # back key setting
                capture_back_loc = pyautogui.center(capture_back[0])

                if try_count > 5 and curr_screen == pos_screen:
                    dataset['file_name_list'] = ['\win_close']
                    win_close = find_location_accuracy(dataset, 0.80)

                    if len(win_close) > 0:
                        if not is_board(dataset):
                            win_close_Loc = pyautogui.center(win_close[0])
                            pyautogui.click(win_close_Loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "윈도우 QUIT : CLEAR")
                            try_count = 0
                            time.sleep(3)
                        else:
                            channel_main_flag = True
                    else:
                        if len(capture_back) > 0:
                            if not is_board(dataset):
                                print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 0 : CLEAR")
                                pyautogui.click(capture_back_loc)
                            else:
                                channel_main_flag = True
                            pyautogui.click(capture_back_loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 1 : CLEAR")
                            try_count = 0
                            time.sleep(3)
                else:
                    if not is_board(dataset):
                        if not is_my_view(dataset):
                            pyautogui.click(capture_back_loc)
                            print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN : CLEAR")
                            try_count = try_count + 1
                            pos_screen = getPixel()
                        else:
                            pyautogui.click(dataset['my_channel'])
                            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, 채널 재 입장")
                    else:
                        #pyautogui.click(dataset['last_location'])
                        #print(str(datetime.now().strftime("%X")) + " : " + "현재위치 내 채널 메인, 마지막 액션 재 실행")
                        channel_main_flag = True
            else:
                print(str(datetime.now().strftime("%X")) + " : " + "BACK BTN 확인 불가 : FAIL")
                return
        else:
            channel_main_flag = True

    while not next_step:

        # 구글 팝업인지 체크
        dataset['file_name_list'] = ['\google_play']
        google_play = find_location_accuracy(dataset, 0.70)

        dataset['file_name_list'] = ['\google_play_x']
        google_play_x = find_location_accuracy(dataset, 0.70)

        if len(google_play) > 0 and len(google_play_x) > 0:
            google_play_x_loc = pyautogui.center(google_play_x[0])
            pyautogui.click(google_play_x_loc)
            print(str(datetime.now().strftime("%X")) + " : " + "DELETE 구글 팝업 : CLEAR")

        # 옵션 페이지 리프레시 (광고 변경)
        dataset['file_name_list'] = ['\page_refresh_option']
        board_option = find_location_accuracy(dataset, 0.80)
        if len(board_option) > 0:
            board_option_loc = pyautogui.center(board_option[0])
            pyautogui.doubleClick(board_option_loc)
            print(str(datetime.now().strftime("%X")) + " : " + "재기동 옵션 버튼 실행 : CLEAR")
            time.sleep(0.5)

            page_refresh_flag = False
            while not page_refresh_flag:
                dataset['file_name_list'] = ['\page_refresh']
                page_refresh = find_location_accuracy(dataset, 0.85)
                if len(page_refresh) > 0:
                    page_refresh_loc = pyautogui.center(page_refresh[0])
                    pyautogui.click(page_refresh_loc)
                    print(str(datetime.now().strftime("%X")) + " : " + "페이지 새로고침 : CLEAR")
                    page_refresh_flag = True
                    dataset['is_refresh'] = True
                else:
                    pyautogui.doubleClick(board_option_loc)
                    print(str(datetime.now().strftime("%X")) + " : " + "재기동 옵션 버튼 재실행 : CLEAR")
                    time.sleep(0.5)

            # 마지막 액션을 다시 수행
            time.sleep(1)
            pyautogui.click(dataset['last_location'])
            print(str(datetime.now().strftime("%X")) + " : " + "액션 재 실행 : CLEAR")

            next_step = True

    return next_step


def find_heart(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "좋아요 처리 모듈 실행")

    # 함수 실행 결과 값
    result = False

    init = dataset['start']

    # My View 화면인지 세팅 아이콘으로 판단
    dataset['file_name_list'] = ['\setting_icon', '\setting_icon1']
    setting_icon = find_location_accuracy(dataset, 0.80)  # 옵션 닷 버튼 찾기

    if len(setting_icon) > 0:
        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰")
        if not init:
            print(str(datetime.now().strftime("%X")) + " : " + "다음 채널 선택")
            win_activate(dataset)
            pyautogui.moveTo(dataset['scroll_base'])
            dataset['file_name_list'] = ['\option_dots']
            option_dots = find_location_accuracy(dataset, '0.70')  # 옵션 닷 버튼 찾기

            if len(option_dots) > 0:
                print(str(datetime.now().strftime("%X")) + " : " + "좋아요 위치 기준점 확인")
                # 0은 첫번째 보드 이미 진행 완료한 건
                # 1은 다음 보드
                real_loc_cnt = 0
                for location in option_dots:
                    location = pyautogui.center(location)
                    if 425 < location.y and 410 < location.x:
                        target = location
                        real_loc_cnt = real_loc_cnt + 1
                        break

                if real_loc_cnt > 0:
                    print(str(datetime.now().strftime("%X")) + " : " + "다음 채널 좋아요 확인")

                    title_loc = (target.x, target.y - 40)

                    win_activate(dataset)
                    pyautogui.moveTo(title_loc)
                    pyautogui.click(title_loc)
                    pyautogui.mouseDown()
                    setting_icon_loc = pyautogui.center(setting_icon[0])
                    setting_icon_loc = (setting_icon_loc.x, setting_icon_loc.y + 65)
                    pyautogui.moveTo(setting_icon_loc)
                    time.sleep(1)
                    pyautogui.mouseUp()
                    time.sleep(1)
                    print(str(datetime.now().strftime("%X")) + " : " + "다음 채널 위치로 이동 완료")
                    result = True
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "다음 채널 좋아요 위치 확인 불가 SCROLL 검색 실행")
                    for idx in range(0, 3):
                        pyautogui.scroll(-500)
                    # time.sleep(0.5)
            else:
                print(str(datetime.now().strftime("%X")) + " : " + "좋아요 위치 기준점 확인 불가")
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "첫번째 채널 선택")
            result = True
    else:
        print(str(datetime.now().strftime("%X")) + " : " + "마이뷰 화면이 아닙니다.")
    return result


# PROCESS MOUDLES
# 좋아요 클릭 모듈
def select_channel(dataset):
    result = False

    print(str(datetime.now().strftime("%X")) + " : " + "현재 채널 진입 모듈 시작")

    next_step = False

    # win_activate(dataset)
    # dataset['file_name_list'] = ['\heart_empty', '\heart_empty1', '\heart_empty2', '\heart_empty3']
    print(str(datetime.now().strftime("%X")) + " : " + "좋아요 클릭 현황 파악")
    dataset['file_name_list'] = ['\heart_empty']
    heart_empty = find_location_detail(dataset, 0.70, 250, 250, 315, 990)

    dataset['file_name_list'] = ['\heart_full']
    heart_full = find_location_detail(dataset, 0.80, 250, 250, 315, 990)

    if len(heart_empty) > 0 or len(heart_full) > 0:
        print(str(datetime.now().strftime("%X")) + " : " + "좋아요 클릭 상태 파악 완료")
        full_heart = False
        empty_x = 0
        empty_y = 0
        full_x = 0
        full_y = 0

        if len(heart_empty) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "클릭 안된 좋아요 연산 중...")
            for loc in heart_empty:
                this_loc = pyautogui.center(loc)
                if (this_loc.y < empty_y or empty_y == 0) and this_loc.x < 450:
                    empty_x = this_loc.x
                    empty_y = this_loc.y

        if len(heart_full) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "클릭된 좋아요 연산 중...")
            for loc in heart_full:
                this_loc = pyautogui.center(loc)
                if (this_loc.y < full_y or full_y == 0) and this_loc.x < 450:
                    full_x = this_loc.x
                    full_y = this_loc.y

        # 좋아요 클릭된 하트의 값이 좋아요 클릭되지 않은 하트보다 상단에 있을 경우
        # 이미 클릭된 하트로 판단
        # 둘다 존재할 경우
        if len(heart_empty) > 0 and len(heart_full) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "모든 상태의 좋아요 존재, 좋아요 선택 기준 연산 중...")
            if full_y == 0:
                full_y = 9999
            if empty_y == 0:
                empty_y = 9999

            if empty_y < full_y:
                print(str(datetime.now().strftime("%X")) + " : " + '현 채널 : 좋아요 클릭 대상')
                curr_loc = (empty_x, empty_y)
            else:
                print(str(datetime.now().strftime("%X")) + " : " + '현 채널 : 좋아요 클릭 비대상')
                curr_loc = (full_x, full_y)
                full_heart = True
        elif len(heart_empty) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "현 채널 : 좋아요 클릭 대상")
            curr_loc = (empty_x, empty_y)
        elif len(heart_full) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "현 채널 : 좋아요 클릭 비대상")
            curr_loc = (full_x, full_y)
            full_heart = True
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "현 채널 : 좋아요 판단 불가 ERROR")
            sys.exit("현 채널 : 좋아요 판단 불가 ERROR")

        # 좋아요 콘텐츠 클릭 처리 로직
        if not full_heart:
            print(str(datetime.now().strftime("%X")) + " : " + "좋아요 클릭 완료")
            pyautogui.click(curr_loc)
            if not capture_module(dataset):
                print(str(datetime.now().strftime("%X")) + " : " + "캡처 실패 모듈 재 실행")
                return False
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "좋아요 클릭 패스")
            if not capture_module(dataset):
                print(str(datetime.now().strftime("%X")) + " : " + "캡처 실패 모듈 재 실행")
                return False

        dataset['file_name_list'] = ['\option_dots']
        option_dots = find_location_accuracy(dataset, 0.85)  # 옵션 닷 버튼 찾기
        print(str(datetime.now().strftime("%X")) + " : " + "채널 보드 위치 파악 중")
        if len(option_dots) > 0:

            print(str(datetime.now().strftime("%X")) + " : " + "채널 보드 위치 계산 중")

            option_loc_x = 0
            option_loc_y = 0
            for loc in option_dots:
                this_loc = pyautogui.center(loc)
                if (this_loc.y < option_loc_y or option_loc_y == 0) and this_loc.x < 450:
                    option_loc_x = this_loc.x
                    option_loc_y = this_loc.y

            channel_loc = (option_loc_x, option_loc_y + 30)
            print(str(datetime.now().strftime("%X")) + " : " + "채널 보드 위치 계산 완료 : " + str(channel_loc))

            dataset['my_channel'] = channel_loc
            print(str(datetime.now().strftime("%X")) + " : " + "채널 보드 위치 BACK UP 완료")

            pyautogui.click(channel_loc)
            print(str(datetime.now().strftime("%X")) + " : " + "채널 클릭 완료.")

            init = True
            while not next_step:
                set_time_out = timeout(dataset)
                if check_timeout(set_time_out):
                    if init:
                        print(str(datetime.now().strftime("%X")) + " : " + "채널 입장 중...")
                        init = False

                    set_time_out2 = timeout(dataset)
                    if check_timeout(set_time_out2):

                        if is_board(dataset):
                            result = True
                            next_step = True
                            print(str(datetime.now().strftime("%X")) + " : " + "채널 입장 완료")
                    else:
                        if is_my_view(dataset):
                            print(str(datetime.now().strftime("%X")) + " : " + "채널 입장 대기 시간 초과, 채널 진입 모듈 재시작")
                            next_step = True
                        else:
                            print(str(datetime.now().strftime("%X")) + " : " + "채널 입장 대기 시간 초과, 마이뷰 인식 불가 ERROR")
                            sys.exit("채널 입장 대기 시간 초과, 마이뷰 인식 불가 ERROR")
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "채널 입장 대기 시간 초과, 재 실행")
                    refresh_reload(dataset)
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "채널 보드 위치 파악 불가")
    return result


# 보드 클릭 모듈
def click_contents(dataset):
    result = False

    print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 진입 모듈 시작")

    dataset['file_name_list'] = ['\split_line', '\split_line1']
    channel_split_line = find_location_accuracy(dataset, 0.70)  # 채널 메인 옵션 닷 찾기

    print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 위치 찾는 중...")

    if len(channel_split_line) > 0:

        print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 위치 확인 완료")

        title_x = 0
        title_y = 0

        print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 정밀 위치 계산 중...")

        for loc in channel_split_line:
            this_loc = pyautogui.center(loc)
            if this_loc.x < 450 and this_loc.y > 250:
                if this_loc.y < title_y or title_y == 0:
                    title_x = this_loc.x
                    title_y = this_loc.y

        if title_x > 0 and title_y > 0:

            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 정밀 위치 보정 값 계산 중...")
            title_loc = (title_x - 150, title_y + 30)
            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 정밀 위치 계산 완료 : " + str(title_loc))

            set_time_out = timeout(dataset)
            check_times = 0
            next_step = False
            while not next_step:

                if check_timeout(set_time_out):
                    if is_board(dataset):
                        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 : 채널 메인")
                        if check_times > 0:
                            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 위치 정밀 위치 후처리 계산 중...")
                            title_loc = (title_loc[0], title_loc[1] + 10)
                            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 위치 정밀 위치 후처리 계산 완료 : " + str(check_times) + " 번째 계산")

                        if is_board(dataset):
                            dataset['last_location'] = title_loc
                            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 정밀 위치 BACK UP 완료")
                            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 클릭 실행")
                            pyautogui.click(title_loc)
                            check_times = check_times + 1
                            time.sleep(1)

                            if not is_board(dataset):
                                if is_loaded(dataset):
                                    print(str(datetime.now().strftime("%X")) + " : " + "페이지 로드 완료")
                                    result = True
                                    next_step = True
                                else:
                                    print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 입장 TIMEOUT")
                                    next_step = True
                        else:
                            if not is_my_view(dataset):
                                if is_loaded(dataset):
                                    print(str(datetime.now().strftime("%X")) + " : " + "페이지 로드 완료")
                                    result = True
                                    next_step = True
                                else:
                                    print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 입장 TIMEOUT")
                                    next_step = True
                    else:
                        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 파악 불가, 컨텐츠 진입 모듈 재 실행")
                        refresh_reload(dataset)
                else:
                    print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 진입 대기 시간 초과, 컨텐츠 진입 모듈 재 실행")
                    next_step = True
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "컨텐츠 정밀 위치 파악 실패, 컨텐츠 진입 모듈 재 실행")

    return result


# 상단 광고 클릭 모듈
def click_top_ad(dataset):
    print(str(datetime.now().strftime("%X")) + " : " + "상단 광고 모듈 실행")
    result = False

    # 보드 텍스트 기준 상단광고 위치 찾기
    if is_board(dataset):
        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 메인 채널")
        dataset['file_name_list'] = ['\main_board_txt']
        board_txt = find_location_accuracy(dataset, 0.75)
        top_ad_x = 0
        top_ad_y = 0
        for loc in board_txt:
            this_loc = pyautogui.center(loc)
            if this_loc.y < 150 or top_ad_y == 0:
                top_ad_y = this_loc.y
                top_ad_x = this_loc.x
                print(str(datetime.now().strftime("%X")) + " : " + "상단 광고 위치 확인 : " + str(top_ad_x) + ", " + str(top_ad_y))

        top_ad_loc = (top_ad_x, top_ad_y + 70)
        dataset['last_location'] = top_ad_loc

        pyautogui.click(top_ad_loc)
        print(str(datetime.now().strftime("%X")) + " : " + "상단 광고 진입 실행")

        if is_loaded(dataset):
            print(str(datetime.now().strftime("%X")) + " : " + "상단 광고 로드 완료")
            result = True
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "상단 광고 로드 실패")
    else:
        if is_my_view(dataset):
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, 채널 재 입장")
            pyautogui.click(dataset['my_channel'])
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "현재위치 찾을 수 없음 모듈 재 실행")

    return result


# 하단 광고 클릭 모듈
def click_bottom_ad(dataset):

    result = False
    print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 모듈 실행")

    win_activate(dataset)
    dataset['return_my_view'] = True
    pyautogui.moveTo(dataset['scroll_base'])

    print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 계산 중...")
    dataset['file_name_list'] = ['\similar_msg_txt', '\similar_msg_txt1']
    similar_msg_txt_loc = find_location_accuracy(dataset, 0.70)

    # 이 채널의 다른보드 메시지 찾기
    dataset['file_name_list'] = ['\other_msg_txt', '\more_kakaoview_txt', '\more_kakaoview_txt1']
    other_msg_txt_loc = find_location_accuracy(dataset, 0.70)

    if is_board(dataset):
        print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 메인 채널")
        if len(other_msg_txt_loc) == 0 and len(similar_msg_txt_loc) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 확인1")
            bottom_ad_loc = pyautogui.center(similar_msg_txt_loc[0])
            bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 140)

            dataset['last_location'] = bottom_ad_loc
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 BACK UP 완료")
            pyautogui.click(bottom_ad_loc)
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 입장 중...")

            if is_loaded(dataset):
                print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 입장 완료")
                result = True
        elif len(other_msg_txt_loc) > 0:
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 확인2")

            # 하단에 광고가 위치할 수 도 있기에 어느정도를 스크롤한다.
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 정밀 조정 중...")
            pyautogui.moveTo(dataset['scroll_base'])
            for i in range(1, 8):
                pyautogui.scroll(-500)
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 정밀 조정 완료")

            # 이 채널의 다른보드 메시지 다시 찾기 위에서 스크롤 이동함
            dataset['file_name_list'] = ['\other_msg_txt']
            other_msg_txt_loc = find_location_accuracy(dataset, 0.70)

            dataset['file_name_list'] = ['\more_kakaoview_txt', '\more_kakaoview_txt1']
            more_kakaoview_loc = find_location_accuracy(dataset, 0.70)
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 정밀 계산 중...")
            if len(other_msg_txt_loc) > 0:
                bottom_ad_loc = pyautogui.center(other_msg_txt_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y + 400)
            elif len(more_kakaoview_loc) > 0:
                bottom_ad_loc = pyautogui.center(more_kakaoview_loc[0])
                bottom_ad_loc = (bottom_ad_loc.x + 50, bottom_ad_loc.y - 100)

            if len(other_msg_txt_loc) > 0 or len(more_kakaoview_loc) > 0:
                print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 정밀 계산 완료")

                dataset['last_location'] = bottom_ad_loc
                print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 BACK UP 완료")
                pyautogui.click(bottom_ad_loc)
                print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 입장 중..")

                if is_loaded(dataset):
                    print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 입장 완료")
                    result = True
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 확인 불가")
            if not is_my_view(dataset):
                print(str(datetime.now().strftime("%X")) + " : " + "하단 광고 위치 재 조정 실행")
                for idx in range(0, 3):
                    pyautogui.scroll(-500)
                time.sleep(1)
            else:
                pyautogui.click(dataset['my_channel'])
                print(str(datetime.now().strftime("%X")) + " : " + "현재 위치 마이뷰, 마지막 보드 재 진입")
    else:
        if not is_my_view(dataset):
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치가 메인 채널이 아닙니다. 메인 채널로 복귀 실행")
            action_back(dataset)
        else:
            print(str(datetime.now().strftime("%X")) + " : " + "현재 위치가 마이뷰 입니다.")
            sys.exit(str(datetime.now().strftime("%X")) + " : " +
                     "하단 광고 모듈에서 현재 위치가 마이뷰 입니다. 더 이상 프로세스를 진행 할 수 없습니다.")


    return result


def activate_auto_tour():
    #time.sleep(5)

    # 과거 정보
    dataset = {"reservation": "202210270601",
               "accuracy": 0.95, "mobile_type": '\s20plus', "speed": 0.5, "limit_time": 5, "scroll_speed": 0.5,
               "scroll_count": 2, "mouse_scroll_cnt": 5, "return_my_view": False, "loading_wait_time": 3,
               # "loading_img_list": ['\loading_bar1', '\loading_bar2', '\loading_bar3', '\loading_bar4', '\loading_bar5',
               #                     '\loading_bar6', '\loading_bar7', '\loading_bar8', '\loading_bar9'],
               "loading_img_list": ['\loading_master'],
               "more_kakao_board": ['\more_kakaoview_txt', '\more_kakaoview_txt1'],
               'file_name_list': ['\home_for_scroll_base', '\home_for_scroll_base1'],
               'loading_msg': False,
               'is_refresh': False,
               'win_title': ['상민의 Galaxy S20+ 5G', 'Galaxy S20 5G', '수윤의 S20']
               }

    dataset['filename_option'] = option_figure(dataset)

    home_for_scroll = find_location_accuracy(dataset, 0.75)
    home_for_scroll = pyautogui.center(home_for_scroll[0])
    home_for_scroll = (home_for_scroll.x, home_for_scroll.y - 400)
    dataset['scroll_base'] = home_for_scroll

    # 예약 시작 모듈
    reservation_starter(dataset)

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
            # 메인하트 찾기
            next_step = find_heart(dataset)

        next_step = False
        while not next_step:
            # My 뷰 채널 진입
            next_step = select_channel(dataset)

        next_step = False
        while not next_step:
            # 채널 컨텐츠 진입
            next_step = click_contents(dataset)

        next_step = False
        set_time_out = datetime.now() + timedelta(seconds=10)
        while not next_step:
            # 캡처 실행
            if check_timeout(set_time_out):
                next_step = capture_back(dataset)
            else:
                refresh_reload(dataset)
                set_time_out = datetime.now() + timedelta(seconds=10)

        next_step = False
        while not next_step:
            # 뒤로 가기 모듈 실행
            dataset['return_my_view'] = False
            next_step = back_to_home(dataset)

        next_step = False
        while not next_step:
            # 상단광고 클릭
            next_step = click_top_ad(dataset)

        next_step = False
        set_time_out = datetime.now() + timedelta(seconds=10)
        while not next_step:
            # 캡처 실행
            if check_timeout(set_time_out):
                next_step = capture_back(dataset)
            else:
                refresh_reload(dataset)
                set_time_out = datetime.now() + timedelta(seconds=10)

        next_step = False
        while not next_step:
            # 뒤로 가기 모듈 실행
            dataset['return_my_view'] = False
            next_step = back_to_home(dataset)

        next_step = False
        while not next_step:
            # 하단광고 클릭
            next_step = click_bottom_ad(dataset)

        next_step = False
        set_time_out = datetime.now() + timedelta(seconds=10)
        while not next_step:
            # 캡처 실행
            if check_timeout(set_time_out):
                next_step = capture_back(dataset)
            else:
                refresh_reload(dataset)
                set_time_out = datetime.now() + timedelta(seconds=10)

        next_step = False
        while not next_step:
            # 뒤로 가기 모듈 실행
            dataset['return_my_view'] = True
            next_step = back_to_home(dataset)


activate_auto_tour()
