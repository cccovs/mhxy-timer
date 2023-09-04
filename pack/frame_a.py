import tkinter as tk

from tkinter import ttk

class frame_a(ttk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(master=root)
        label = ttk.Label(self, text='勾选要提醒的项目', background='#2d2d2d', foreground='#ffffff', font=('微软雅黑', 13))
        label.pack(anchor='nw')
        label.bind('<Double-Button-1>', lambda event: root.geometry('+{}+{}'.format(root.winfo_screenwidth()-450, 0)))
        label.bind('<Enter>', lambda event: self.trigger_event(event))
        label.bind('<Leave>', lambda event: self.trigger_event(event))

        self.checkbutton_values = [tk.BooleanVar(self, value=True) for _ in range(4)]
        self.checkbutton_objs: list[ttk.Checkbutton] = []
        for i, item in enumerate(('日常', '地煞', '元辰', '护符')):
            temp = ttk.Checkbutton(self, text=item, onvalue=True, offvalue=False, variable=self.checkbutton_values[i])
            temp.pack(anchor='sw', side='left')
            self.checkbutton_objs.append(temp)

        self.content = tk.StringVar()
        self.bottom_label = ttk.Label(root, textvariable=self.content, font=('宋体', 8))
        self.bottom_label.pack(side='bottom', anchor='sw', padx=5)


    def trigger_event(self, event: tk.Event):
        if event.type == '7':
            self.content.set('双击移动到右上角')
        else:
            self.content.set('')

    def get_select(self):
        return list(map(lambda x: x.get(), self.checkbutton_values))
    
    def disabled(self):
        for _ in map(lambda x: x.configure(state=tk.DISABLED), self.checkbutton_objs):
            pass

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('450x300+1200+550')
    frame_a(root=root).place(x=0, y=0)
    root.mainloop()