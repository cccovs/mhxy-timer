# 作者 CCCOVS

import queue

from op import speaker

class consumer_task:
    def __init__(self) -> None:
        self.tts = speaker.TTS()

    def run(self, Q: queue.Queue):
        while True:
            msg = Q.get()
            self.tts.say(msg)

    def change_rate(self, speed_up: bool):
        if speed_up:
            self.tts.rate = 2
        else:
            self.tts.rate = 0