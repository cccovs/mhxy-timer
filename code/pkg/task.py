# 作者 CCCOVS

import queue

import pyttsx3

class consumer_task:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 135)

    def run(self, Q: queue.Queue):
        while True:
            msg = Q.get()
            self.engine.say(msg)
            self.engine.runAndWait()

    def change_rate(self, speed_up: bool):
        if speed_up:
            self.engine.setProperty('rate', 220)
        else:
            self.engine.setProperty('rate', 135)