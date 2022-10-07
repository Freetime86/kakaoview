# GUI 생성
import tkinter
import tkinter.ttk as ttk
import supportModule as sm
import queue #MK: queue를 사용하기 위해 추가
from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime
import threading
import time
import sys
from PyQt5.QtCore import *
import time
import sys

import kakaoTabs
import main


#쓰레드 선언
class Thread1(QThread):
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent):
        super().__init__(parent)
    def run(self):
        main.main_process(dataset)


class MainWidget:
    def __init__(self):
        super().__init__()
        self.win = tkinter.Tk()

        # win = tkinter.Tk()
        self.win.title('카카오뷰 자동 시스템')
        self.win.option_add("*Font", "맑은고딕 10")  # 폰트설정
        self.win.geometry('500x600')
        self.win.resizable(False, False)

    def active(self):
        format_date = calendar.get_date().strftime("%Y%m%d")
        if tab_combobox.get() == '카카오탭 선택':
            tkinter.messagebox.showwarning(title='태그 선택 오류', message="지정할 탭 값을 선택 하세요.!")
            return
        elif site_combobox.get() == '사이트 선택':
            tkinter.messagebox.showwarning(title='웹페이지 정보 오류', message="데이터를 긁어오기 위한 웹사이트를 지정하세요.")
            return
        elif kakao_id.get() == '' or kakao_pw.get() == '':
            tkinter.messagebox.showwarning(title='ID 또는 PW 오류', message="카카오 계정정보를 입력해 주세요.")
            return

        global dataset
        # 파라미터 맵핑
        dataset = {"sel_tab": tab_combobox.get(),
                   "sel_site": site_combobox.get(),
                   "user_id": kakao_id.get(),
                   "user_pw": kakao_pw.get(),
                   "sel_date": format_date,
                   "sel_hour": hour_combobox.get(),
                   "sel_min": min_combobox.get(),
                   "jump_time": time_combobox.get(),
                   "except_list": sm.split_input_data(except_channel.get("1.0", tkinter.END)),
                   "srt_seq": srt_seq.get(),
                   "loop_cnt": loop_cnt.get()
                   }

        print(dataset)
        # 메인 프로세스 실행
        #run_thread("__main__", dataset)
        #main.main_process(dataset)
        x = Thread1(self)
        x.start()

    def reset(self):
        global win

        try:
            if ('normal' == win.state()):
                win.destroy()
        finally:
            win = tkinter.Tk()
            win.title('카카오뷰 자동 시스템')
            win.option_add("*Font", "맑은고딕 10")  # 폰트설정
            win.geometry('500x600')
            win.resizable(False, False)

            # GUI 정보 만들기
            self.make_frame()

    def stupid(self):
        return

    def time_change(self):
        result = True
        if int(now.hour) > int(hour_combobox.get()):
            tkinter.messagebox.showwarning(title='시간 설정 확인', message="현재 시간보다 작게 설정할 수 없습니다.")
            result = False
        elif int(now.minute) > int(min_combobox.get()) and int(now.hour) >= int(hour_combobox.get()):
            tkinter.messagebox.showwarning(title='시간 설정 확인', message="현재 시간보다 작게 설정할 수 없습니다.")
            result = False

        if not result:
            hour_combo_text.set(pre_hour_combobox.get())
            min_combo_text.set(pre_min_combobox.get())
            time_combo_text.set(pre_time_combobox.get())
        else:
            pre_hour_combobox.set(hour_combobox.get())
            pre_min_combobox.set(min_combobox.get())
            pre_time_combobox.set(time_combobox.get())

        # 가능 수량 재 계산
        self.cal_loop_cnt()

    def cal_loop_cnt(self):
        cal_conut = round((24 - int(hour_combobox.get())) / int(time_combobox.get()))
        # 카카오뷰 max 수량정책
        if cal_conut > 10:
            cal_conut = 10
        loop_text.set(cal_conut)

    def clock(self):
        clock_text.set("현재 시간 : " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        clock_label.pack()
        clock_label.configure(font=("맑은고딕", 10, "bold"))
        clock_label.place(x=280, y=20, width=200, height=20)
        clock_label.after(1000, self.clock)

    def make_frame(self):
        # 전역 변수 선언 / 초기화 되었을 때 사용하기 위함
        global calendar
        global tab_combobox
        global site_combobox
        global kakao_id
        global kakao_pw
        global except_channel
        global hour_combobox
        global min_combobox
        global time_combobox
        global pre_hour_combobox
        global pre_min_combobox
        global pre_time_combobox
        global srt_seq
        global now
        global set_hour
        global loop_cnt
        global loop_text
        global hour_combo_text
        global min_combo_text
        global time_combo_text
        global clock_label
        global clock_text

        # 탭리스트 호출
        tabList = kakaoTabs.kakaoviewTabList()
        siteList = kakaoTabs.siteList()

        # date 변수
        sel_date = StringVar()

        # 카카오탭
        tabLabel = Label(self.win, text="카카오탭 선택 : ", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=10, width=100, height=20)
        # 탭 콤보
        tab_combobox = ttk.Combobox(self.win, values=tabList, state="readonly", height=15)  # win 창에 콤보박스 생성
        tab_combobox.set('카카오탭 선택')
        tab_combobox.pack()
        tab_combobox.place(x=120, y=10, width=150)

        # 사이트 선택
        tabLabel = Label(self.win, text="사이트 선택 : ", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=40, width=100, height=20)
        # 탭 콤보
        site_combobox = ttk.Combobox(self.win, values=siteList, state="readonly", height=15)
        site_combobox.set('사이트 선택')
        site_combobox.pack()
        site_combobox.place(x=120, y=40, width=150)

        # 카카오 계정정보 입력
        tabLabel = Label(self.win, text="카카오 ID : ", anchor="w")
        tabLabel.place(x=20, y=70, width=100, height=20)

        kakao_id = Entry(self.win, width=30)
        kakao_id.pack()
        kakao_id.place(x=120, y=70, width=150, height=20)

        tabLabel = Label(self.win, text="카카오 PW : ", anchor="w")
        tabLabel.place(x=20, y=100, width=100, height=20)

        kakao_pw = Entry(self.win, width=30, show='*')
        kakao_pw.pack()
        kakao_pw.place(x=120, y=100, width=150, height=20)

        # clock
        clock_text = StringVar()
        clock_label = Label(self.win, textvariable=clock_text, anchor="center")
        clock_label.after(1000, self.clock)

        # DATE PICKER 패킹
        tabLabel = Label(self.win, text="보드발행 지정일 선택", anchor="center")
        tabLabel.pack()
        # tabLabel.configure(font=("맑은고딕", 11, "bold"))
        tabLabel.place(x=300, y=60, width=150, height=20)

        calendar = DateEntry(self.win, width=16, background="magenta3", foreground="white", bd=2, date_pattern='yyyy/mm/dd')
        calendar.pack(pady=20)
        calendar.place(x=325, y=90, width=100, height=20)

        # 사이트 선택
        tabLabel = Label(self.win, text="사이트 선택 : ", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=40, width=100, height=20)
        # 탭 콤보
        site_combobox = ttk.Combobox(self.win, values=siteList, state="readonly", height=15)
        site_combobox.set('사이트 선택')
        site_combobox.pack()
        site_combobox.place(x=120, y=40, width=150)

        # 수기 시간 세팅
        tabLabel = Label(self.win, text="배포 시간 세팅 (기본 값 사용 권장 오전04~오후22시)", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=130, width=460, height=20)
        tabLabel = Label(self.win, text="※ 10개 발행 기준 24 시가 넘어서면 발행되지 않는다. [ex. 2시간 X 10개]", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=150, width=460, height=20)

        # 시간 콤보
        # 현재 시간 기준으로 30분 기점 오버일 때 2시간 UP 그외는 1시간 후를 기본 값으로 설정
        now = datetime.now()
        set_hour = now.hour
        if int(now.hour) >= 4:
            if int(now.minute) > 30:
                set_hour = int(set_hour) + 2
            else:
                set_hour = int(set_hour) + 1
        # 백업 이전 값
        hour_combo_text = StringVar()
        pre_hour_combobox = StringVar()
        pre_hour_combobox.set(str(set_hour))
        tabLabel = Label(self.win, text="시작 시간", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=180, width=70, height=20)
        hour_combobox = ttk.Combobox(self.win, state="readonly", height=15, textvariable=hour_combo_text,
                                     values=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                                             '22', '23'])
        hour_combobox.set(str(set_hour))
        hour_combobox.bind("<<ComboboxSelected>>", self.time_change)
        hour_combobox.pack()
        hour_combobox.place(x=90, y=180, width=40)
        tabLabel = Label(self.win, text="시", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=130, y=180, width=30, height=20)

        # 분 콤보
        # 백업 이전 값
        min_combo_text = StringVar()
        pre_min_combobox = StringVar()
        pre_min_combobox.set('00')
        min_combobox = ttk.Combobox(self.win, state="readonly", height=15, textvariable=min_combo_text,
                                    values=['00', '10', '20', '30', '40', '50'])
        min_combobox.set('00')
        min_combobox.bind("<<ComboboxSelected>>", self.time_change)
        min_combobox.pack()
        min_combobox.place(x=150, y=180, width=40)
        tabLabel = Label(self.win, text="분", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=190, y=180, width=30, height=20)

        tabLabel = Label(self.win, text="시간 간격", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=230, y=180, width=70, height=20)
        # 시간 점프 단위
        time_combo_text = StringVar()
        pre_time_combobox = StringVar()
        pre_time_combobox.set('2')
        time_combobox = ttk.Combobox(self.win, state="readonly", height=15, textvariable=time_combo_text
                                     , values=['1', '2', '3', '4', '5', '6'])
        time_combobox.set('2')
        time_combobox.bind("<<ComboboxSelected>>", self.time_change)
        time_combobox.pack()
        time_combobox.place(x=300, y=180, width=30)
        tabLabel = Label(self.win, text="시간 단위", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=340, y=180, width=70, height=20)

        tabLabel = Label(self.win, text="시작SEQ(기본 설정 권장 '0')", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=210, width=190, height=20)
        srt_seq = Entry(self.win, width=30)
        srt_seq.insert(0, 0)
        srt_seq.pack()
        srt_seq.place(x=200, y=210, width=40, height=20)

        # 발행 갯수 계산
        # (24시간 - 현재 시간) / 발행 간격
        loop_text = StringVar()
        tabLabel = Label(self.win, text="발행 갯수(자동계산)", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=260, y=210, width=160, height=20)
        loop_cnt = Entry(self.win, width=30, textvariable=loop_text)
        self.cal_loop_cnt()  # 가능 횟수 세팅
        # loop_cnt.configure(state="disable")
        loop_cnt.pack()
        loop_cnt.place(x=390, y=210, width=40, height=20)

        # 제외 채널
        tabLabel = Label(self.win, text="제외 채널 입력 (구분은 콤마{,}로 입력해야 함) [ex:도래미,정보통]", anchor="w")
        tabLabel.pack()
        tabLabel.place(x=20, y=240, width=420, height=20)
        except_channel = scrolledtext.ScrolledText(self.win)
        except_channel.pack()
        except_channel.place(x=20, y=270, width=460, height=80)
        # scroll.insert(tk.INSERT, '안녕하세요' + name.get())
        # self.txbox.insert(INSERT, '안녕하세요')
        # self.txbox.delete(1.0, 'end')  # 내용지우기

        # ACTIVATE BUTTON
        activate_btn = tkinter.Button(self.win, text="보드 발행", command=self.active, anchor="center")
        activate_btn.pack()
        activate_btn.place(x=20, y=550, width=145, height=40)

        # RESET BUTTON
        reset_btn = tkinter.Button(self.win, text="입력 초기화", command=self.reset, anchor="center")
        reset_btn.pack()
        reset_btn.place(x=180, y=550, width=145, height=40)

        # OPTION BUTTON
        option_btn = tkinter.Button(self.win, text="멍텅구리 버튼", command=self.stupid, anchor="center")
        option_btn.pack()
        option_btn.place(x=340, y=550, width=145, height=40)

        self.win.mainloop()

tmp = MainWidget()
tmp.make_frame()



