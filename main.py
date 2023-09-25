import os
import time
import queue
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pyttsx3

from pack.tools import tools
from pack.frame_a import frame_a
from pack.frame_b import frame_b
from pack.frame_c import frame_c

__VERSION__ = 'v2.0.6'
__LAST_UPDATE__ = '2023-09-25'

class consumer_task:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 135)

    def play(self, Q: queue.Queue):
        while True:
            msg = Q.get()
            self.engine.say(msg)
            self.engine.runAndWait()

    def change_rate(self, speed_up: bool):
        if speed_up:
            self.engine.setProperty('rate', 220)
        else:
            self.engine.setProperty('rate', 135)
            

class MainForm:
    def __init__(self) -> None:
        self.Q = queue.Queue()

        root_x, root_y = 450, 300

        self.root = tk.Tk()
        self.root.title('<梦幻手游>时间管理大师 {}'.format(__VERSION__))
        self.root.geometry('{}x{}+{}+{}'.format(root_x, root_y, (self.root.winfo_screenwidth()-root_x)//2, (self.root.winfo_screenheight()-root_y)//2))
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.close_window_event)
        self.root.iconbitmap(tools.get_resource_path('./pack/image/icon/default.ico'))

        self.root.bind('<Button-3>', lambda event: self.post_window(event))

        self.f_a = frame_a(self.root)
        self.f_a.place(x=0, y=0)

        self.f_b = frame_b(self.root)
        self.f_b.place(x=220, y=0)

        self.button_content = tk.StringVar(value='启动')
        self.btn = ttk.Button(self.root, textvariable=self.button_content, command=self.start_event)
        self.btn.place(x=2, y=58, width=root_x-4)

        ttk.Separator(self.root).place(x=2, y=90, width=root_x-4)

        self.f_c = frame_c(self.root, self.Q)
        self.f_c.place(x=0, y=100)

        time.sleep(0.2)
        self.consumer = consumer_task()
        threading.Thread(target=self.consumer.play, args=(self.Q,), daemon=True).start()

        self.root.mainloop()
        
    def post_window(self, event: tk.Event):
        menu = tk.Menu(tearoff=False)
        if self.root.attributes('-topmost'):
            menu.add_command(label='取消置顶', command=lambda: self.root.attributes('-topmost', False))
        else:
            menu.add_command(label='窗口置顶', command=lambda: self.root.attributes('-topmost', True))
            
        menu.post(event.x_root+5, event.y_root+5)

    def close_window_event(self):
        if self.btn.instate((tk.DISABLED, )):
            if messagebox.askyesno('强制关闭', '程序正在运行,是否强制关闭?\n'*3):
                self.root.destroy()
        else:
            self.root.destroy()

    def start_event(self):
        if not any(self.f_a.get_select()):
            messagebox.showwarning('未选择任何项', '未选择任何项')

        self.f_c.init(*self.f_a.get_select())
        
        self.button_content.set('运行中')
        self.btn.configure(state=tk.DISABLED)
        self.f_a.disabled()

        time.sleep(0.2)
        threading.Thread(target=self.run, daemon=True).start()
        

    def run(self):
        self.Q.put('软件已启动')
        while True:
            try:
                timestamp = self.f_c.get_timestamp
            except:
                self.Q.put('活动已全部结束')
                return
            
            if timestamp - time.time() > 180:
                time.sleep(timestamp - time.time() - 180)
                self.Q.put('距离{}, 还有三分钟'.format(self.f_c.get_name))

            if timestamp - time.time() > 60:
                time.sleep(timestamp - time.time() - 60)
                self.Q.put('距离{}, 还有一分钟'.format(self.f_c.get_name))

            if timestamp - time.time() > 10:
                time.sleep(timestamp - time.time() - 5)

                self.consumer.change_rate(True)
                for item in ('five', 'four', 'three', 'two', 'one'):
                    self.Q.put(item)
                    time.sleep(1)
                else:
                    self.consumer.change_rate(False)
            
            if '上古' in self.f_c.get_name:
                if self.f_c.get_optionmenu == '关闭':
                    self.f_c.set_optionmenu(True)
                    self.f_c.optionmenu_event('激活')
                    time.sleep(100)
                    self.f_c.set_optionmenu(False)
                    self.f_c.optionmenu_event('关闭')
                else:
                    self.Q.put('鼠标连点器状态维持')

            self.f_c.delete_row()


def main():
    os.chdir(os.path.dirname(__file__))
    MainForm()

if __name__ == '__main__':
    main()

