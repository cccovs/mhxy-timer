# 作者 CCCOVS

import time
import queue
import random
import threading

import mouse

class mouse_clicker:
    def __init__(self, Q: queue.Queue):
        self.Q = Q
        self.__share = threading.Event()
        self.__run = threading.Event()

    def keep_click(self):
        while True:
            self.__run.wait()
            while self.__run.is_set():
                # 每秒约7 ~ 8次,符合正常按键手速极限,按键行为约5毫秒
                time.sleep(random.uniform(0.12, 0.15))
                mouse.click()

    def change_run_status(self, status: bool):
        if self.__share.is_set():
            if status is True:
                self.__run.set()
                self.Q.put('run')
            else:
                self.__run.clear()
                self.Q.put('stop')

    def change_share_status(self, status: bool):
        if status is True:
            self.__share.set()
        else:
            self.__share.clear()
            time.sleep(0.2)
            self.__run.clear()