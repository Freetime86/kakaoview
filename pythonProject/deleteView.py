import pyautogui
from datetime import datetime, timedelta
from PIL import ImageGrab
import os
import time


def main_process():
    work_dir = os.getcwd() + "\img\delete_view"
    file_ext = ".png"

    no_more = False
    while not no_more:
        hide_btn = pyautogui.locateOnScreen(work_dir + "\hide_btn" + file_ext,
                                            confidence=0.8, region=(340, 170, 410, 1000))
        if hide_btn is not None:
            hide_btn_loc = pyautogui.center(hide_btn)
            pyautogui.click(hide_btn_loc)
            time.sleep(0.3)

        hide_confirm_btn = pyautogui.locateOnScreen(work_dir + "\hide_confirm_btn" + file_ext,
                                                    confidence=0.8, region=(345, 570, 396, 610))
        if hide_confirm_btn is not None:
            confirm_loc = pyautogui.center(hide_confirm_btn)
            pyautogui.click(confirm_loc)


main_process()
