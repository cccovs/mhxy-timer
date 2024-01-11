# 作者: CCCOVS

import time
import tkinter as tk
from tkinter import ttk


class frame_b(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root, width=300)
        self.mutex = False
        self.audio_var = tk.BooleanVar(value=False)
        ttk.Radiobutton(self, text='显示', value=True, variable=self.audio_var, command=self.radiobutton_event).grid(row=0, column=0)
        ttk.Radiobutton(self, text='隐藏', value=False, variable=self.audio_var, command=self.radiobutton_event).grid(row=1, column=0)

        self.label_content = tk.StringVar(value='- -: - -: - -')
        ttk.Label(self, textvariable=self.label_content, font=('ink free', 28), justify='right').grid(row=0, column=1, rowspan=2, padx=(10, 0))

    def radiobutton_event(self):
        def time_loop():
            if self.audio_var.get() is True:
                self.label_content.set(time.strftime('%H:%M:%S'))
                self.after(1000, time_loop)
            else:
                self.mutex = False
                self.label_content.set('- -: - -: - -')

        if self.mutex == self.audio_var.get():
            return
        
        if self.audio_var.get() is True:
            self.mutex = True
            return time_loop()



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('450x300+1200+550')
    frame_b(root=root).place(x=220, y=0)
    root.mainloop()