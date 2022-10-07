import pyautogui
import win32api
import win32gui
import win32con
import win32ui
from ctypes import windll
#import Image

import time
#비활성 클릭 완성 하지만 윈도우 앱에서는 작동 x 물리 키보드를 이용해야함
def click(x, y):
    #hWnd = win32gui.FindWindow(None, "상민의 Galaxy S20+ 5G")
    hWnd = win32gui.FindWindow(None, "NAVER - Chrome")
    #hWnd = win32gui.FindWindow(None, "Netflix")
    lParam = win32api.MAKELONG(x, y)

    hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)


if __name__ == '__main__':
    click(117, 667)