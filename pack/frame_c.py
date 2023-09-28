# 游戏有概率吃掉热键绑定,所以热键需要经常重置
import time
import queue
import random
import calendar
import threading
import tkinter as tk
from tkinter import ttk

import mouse
import keyboard

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
            self.__run.clear()


class frame_c(ttk.Frame):
    def __init__(self, root, Q: queue.Queue):
        super().__init__(master=root)

        self.Q = Q

        self.notebook = ttk.Notebook(self, width=446, height=155, padding=2)
        self.notebook.pack()

        # 活动展示
        style_value = ttk.Style()
        style_value.configure("Treeview", rowheight=25, font=("宋体", 12))
        self.tree = ttk.Treeview(self, show='headings', columns=('name', 'start', 'end'), selectmode='none')
        self.tree.tag_configure('aaa', background='#858585', foreground='#ffffff')  # 灰底白字
        self.tree.tag_configure('bbb', background='#42BAD8', foreground='#ffffff')  # 蓝底白字
        self.tree.tag_configure('ccc', background='#858585', foreground='#ffffff') # 同一

        scroll = ttk.Scrollbar(self.tree, orient='vertical')
        scroll.pack(fill='y', side='right')

        self.tree.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.tree.yview)
        

        self.tree.column('name', width=1)
        self.tree.column('start', width=1, anchor='center')
        self.tree.column('end', width=1, anchor='center')

        self.tree.heading('name', text='活动')
        self.tree.heading('start', text='开始')
        self.tree.heading('end', text='结束')

        self.tree.insert('', index=tk.END, values=('---', '00:00:00', '00:00:00'))

        # 鼠标连点器
        frame = ttk.Frame()
        self.content = tk.StringVar(value='关闭')
        self.option = ttk.OptionMenu(frame, self.content, '关闭', '关闭', '激活', command=self.optionmenu_event)
        self.option.pack(anchor='nw')

        self.label1 = ttk.Label(frame, text='- 热键 -\n<F1>: 运行\n<F2>: 停止\n\n- 说明 -\n此状态在勾选<护符>项后会动态激活与关闭,无需手动操作', anchor='nw', padding=5, background='#3786AE', foreground='#ffffff', width=60)
        self.label1.pack(anchor='nw')

        self.label2 = ttk.Label(frame, text='- 热键 - \n<F1>: 运行\n<F2>: 停止\n\n- 说明 -\n建议临时使用此功能,使用完后手动切换到<关闭>模式', anchor='nw', padding=5, background='#000000', foreground='#FB0000', width=60)
        
        # 记事本
        self.text = tk.Text(font=('宋体', 14))

        # 临时闹钟
        frame2 = ttk.Frame()
        frame2_1 = ttk.Frame(frame2, padding=5)
        frame2_1.pack(anchor='nw')

        self.clock_content = tk.StringVar()
        entry1 = ttk.Entry(frame2_1, textvariable=self.clock_content, font=('微软雅黑', 11))

        self.checkbutton1_var = tk.BooleanVar(value=False)
        self.checkbutton1 = ttk.Checkbutton(frame2_1, onvalue=True, offvalue=False, variable=self.checkbutton1_var, command=lambda: entry1.configure(state=tk.DISABLED) if self.checkbutton1_var.get() else entry1.configure(state=tk.NORMAL))

        self.btn1 = ttk.Button(frame2_1, text='启动', width=4)

        self.checkbutton1.pack(side='left', anchor='nw')
        entry1.pack(side='left', anchor='nw')
        self.btn1.pack(side='left', anchor='nw', padx=(5, 0))

        
        
        # 关于
        label3 = ttk.Label(text='软件作者: cccovs\n系统要求: windows10 x64或以上.\n\n开源项目地址:\n-- https://github.com/cccovs/mhxy-timer\n-- https://gitee.com/cccovs/mhxy-timer', anchor='nw', padding=(0, 5, 0, 0))
        
        # 添加组件
        self.notebook.add(self.tree, text='进行时')
        self.notebook.add(frame, text='鼠标连点器')
        self.notebook.add(self.text, text='记事本')
        self.notebook.add(frame2, text='临时闹钟')
        self.notebook.add(label3, text='关于')

        time.sleep(0.2)
        # 加载连点器线程
        self.clicker = mouse_clicker(self.Q)
        threading.Thread(target=self.clicker.keep_click, daemon=True).start()
        time.sleep(0.1)
    

    def init(self, *args):
        '''
        加载活动列表详情
        '''
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 日常, 地煞, 元辰, 护符
        self.richang = ({'帮派强盗   ': ('12:30:00', '--:--:--'), '竞技场活动1': ('13:00:00', '14:00:00'), '门派争霸  ': ('21:00:00', '21:40:00'), 
                         '竞技场活动2': ('22:00:00', '23:00:00')},

                        {'帮派百草谷 ': ('12:30:00', '13:00:00'), '帮派答题   ': ('20:20:00', '20:30:00'), '帮派竞赛  ': ('21:00:00', '22:00:00')},

                        {'九黎演武   ': ('12:15:00', '13:00:00'), '风云竞技场1': ('13:00:00', '14:00:00'), '召唤灵乐园': ('21:00:00', '21:40:00'), 
                         '风云竞技场2': ('22:00:00', '23:00:00')},

                        {'帮派百草谷 ': ('12:30:00', '13:00:00'), '帮派答题   ': ('20:20:00', '20:30:00'), '帮派竞赛  ': ('21:00:00', '22:00:00')},

                        {'帮派迷阵   ': ('12:00:00', '14:00:00'), '勇闯迷魂塔 ': ('19:00:00', '22:00:00'), '剑会群英  ': ('20:00:00', '23:00:00')},

                        {'剑会群英   ': ('12:00:00', '20:00:00'), '小猪快跑  ': ('12:00:00', '18:00:00'), '科举会试1   ': ('13:00:00', '--:--:--'), 
                         '科举会试2 ': ('15:00:00', '--:--:--'), '科举会试3   ': ('20:00:00', '--:--:--'), '决战九华山 ': ('21:00:00', '22:00:00'), 
                         '帮派车轮战': ('22:00:00', '23:00:00'), 
                        },

                        {'剑会群英   ': ('12:00:00', '20:00:00'), '帮派秘境  ': ('12:30:00', '13:30:00'), '擂台大挑战 ': ('17:00:00', '20:00:00'), 
                         '梦幻迷城  ': ('18:30:00', '20:00:00'), '比武大会   ': ('21:00:00', '22:20:00'), '比武-结束 ': ('22:20:00', '--:--:--'), 
                         }, )
                

        self.disha = {'地煞1': ('09:30:30', '--:--:--'), '地煞2': ('11:30:30', '--:--:--'), '地煞3': ('13:30:30', '--:--:--'), '地煞4': ('15:30:30', '--:--:--'),
                      '地煞5': ('17:30:30', '--:--:--'), '地煞6': ('19:30:30', '--:--:--'), '地煞7': ('22:30:30', '--:--:--'), '地煞8': ('23:30:30', '--:--:--')}
        
        self.yuanchen = {}
        for i in range(24):
            self.yuanchen['元辰' + str(i)] = ('{}:00:00'.format(str(i).zfill(2)), '--:--:--')

        self.hufu = {'上古灵符1': ('10:10:00', '--:--:--'), '上古灵符2': ('16:10:00', '--:--:--'), 
                     '上古咒符1': ('12:10:00', '--:--:--'), '上古咒符2': ('18:10:00', '--:--:--'), 
                     '上古护符1': ('14:10:00', '--:--:--'), '上古护符2': ('20:10:00', '--:--:--')}
        
        # 初始化活动内容
        self.all_items = {}

        if args[0]:
            self.all_items.update(self.richang[time.localtime().tm_wday])

            month_calendar = calendar.monthcalendar(time.localtime().tm_year, time.localtime().tm_mon)
            # 每月的最后一个星期一(武神坛活动)
            if time.localtime().tm_mday == month_calendar[-1][0]:
                self.all_items.update({'武神坛庆功游行': ('20:00:00', '?:?:?'), '武神坛在线抽奖': ('20:20:00', '?:?:?')})

            # 每月的最后一个周六(科举殿试)
            if month_calendar[-1][5] == 0:
                last_saturday = month_calendar[-2][5]
            else:
                last_saturday = month_calendar[-1][5]

            if time.localtime().tm_mday == last_saturday:
                self.all_items['科举殿试'] = ('20:15:00', '--:--:--')

        if args[1]:
            self.all_items.update(self.disha)

        if args[2]:
            self.all_items.update(self.yuanchen)
        
        if args[3]:
            self.all_items.update(self.hufu)


        self.sort_list = sorted(self.all_items.items(), key=lambda k: k[1][0])

        self.filter_list = filter(lambda item: item[1][0] > time.strftime('%H:%M:%S'), self.sort_list)
        self.ret_lst = map(lambda x: (x[0], *x[1]), self.filter_list)

        self.filter_list2 = filter(lambda item: item[1][0] < time.strftime('%H:%M:%S'), self.sort_list)
        self.ret_lst2 = map(lambda x: (x[0], *x[1]), self.filter_list2)

        self.tree.insert('', tk.END, values=('-- start --', '--------', '--------'))

        for items in self.ret_lst:
            self.tree.insert('', tk.END, values=items)

        self.tree.insert('', tk.END, values=('-- end --', '--------', '--------'))

        for items in self.ret_lst2:
            self.tree.insert('', tk.END, values=items, tags='ccc')

        self.tree.item(self.tree.get_children()[0], tags='aaa')
        self.tree.item(self.tree.get_children()[1], tags='bbb')
        if self.tree.item(self.tree.get_children()[2], 'values')[1] == self.tree.item(self.tree.get_children()[1], 'values')[1]:
            self.tree.item(self.tree.get_children()[2], tags='bbb')

    def optionmenu_event(self, event):
        if event == '激活':
            try: # 防止多次激活
                keyboard.remove_hotkey(self.kb1)
                keyboard.remove_hotkey(self.kb2)
            except:
                pass
            finally:
                self.kb1 = keyboard.add_hotkey('F1', self.clicker.change_run_status, args=(True, ))
                self.kb2 = keyboard.add_hotkey('F2', self.clicker.change_run_status, args=(False, ))

            self.Q.put('鼠标连点器-激活')
            self.label1.pack_forget()
            self.label2.pack(anchor='nw')
            self.clicker.change_share_status(True)  
        else:
            try: # 防止多次关闭或者热键绑定被程序吃掉
                keyboard.remove_hotkey(self.kb1)
                keyboard.remove_hotkey(self.kb2)
            except:
                self.Q.put('绑定的热键被吃掉了')  
            else:
                self.Q.put('鼠标连点器-关闭')

            self.label2.pack_forget()
            self.label1.pack(anchor='nw')
            self.clicker.change_share_status(False) 

    def delete_row(self):
        self.tree.insert('', tk.END, values=self.tree.item(self.tree.get_children()[0])['values'], tags='ccc')
        self.tree.delete(self.tree.get_children()[0])
        self.tree.item(self.tree.get_children()[0], tags='aaa')
        self.tree.item(self.tree.get_children()[1], tags='bbb')

        if self.tree.item(self.tree.get_children()[2], 'values')[1] == self.tree.item(self.tree.get_children()[1], 'values')[1]:
            self.tree.item(self.tree.get_children()[2], tags='bbb')


    def set_optionmenu(self, on: bool):
        '''
        护符调用专属,其它组件禁止调用
        '''
        if on:
            self.content.set('激活')
            self.optionmenu_event('激活')
        else:
            self.content.set('关闭')
            self.optionmenu_event('关闭')

    @property
    def get_optionmenu(self) -> str:
        return self.content.get()
    
    @property
    def get_name(self) -> str:
        '''
        格式化的后名称,删除数字后缀
        处于同时时间的多个活动名称合并
        '''
        time_str1 = self.tree.item(self.tree.get_children()[1], 'values')[1]
        time_str2 = self.tree.item(self.tree.get_children()[2], 'values')[1]
        if time_str1 == time_str2:
            return self.tree.item(self.tree.get_children()[1], 'values')[0].rstrip('0123456789').replace('地', '弟') + '-' + self.tree.item(self.tree.get_children()[2], 'values')[0].rstrip('0123456789').replace('地', '弟')
        else:
            return self.tree.item(self.tree.get_children()[1], 'values')[0].rstrip('0123456789').replace('地', '弟')
    
    @property
    def get_timestamp(self) -> float:
        strtime = self.tree.item(self.tree.get_children()[1], 'values')[1]
        date = time.strftime('%Y-%m-%d', time.localtime())
        datetime = '{} {}'.format(date, strtime)
        struct_time = time.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        return time.mktime(struct_time)

        
if __name__ == '__main__':
    Q = queue.Queue()
    root = tk.Tk()
    root.geometry('450x300+1200+550')
    frame_c(root, Q).place(x=0, y=100)
    root.mainloop()