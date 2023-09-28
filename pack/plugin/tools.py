import os
import sys

class tools:
    @staticmethod
    def get_resource_path(relative_path):
        '''
        根据条件判断是否通过相对路径获取临时目录的绝对路径
        '''
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
            
        return os.path.join(base_path, relative_path)