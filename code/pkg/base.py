import sys
from ctypes import windll as __windll
from pathlib import WindowsPath


def get_resource_path(relative_path: str) -> str:
    '''
    获取文件的真实路径\n
    让pyinstaller可以正确打包
    '''
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        return WindowsPath(base_path, relative_path).__str__()
    else:
        return WindowsPath.absolute(WindowsPath(relative_path)).__str__()
    

def is_admin() -> bool:
    '''
    查询是否具有管理员权限\n
    在win10及以上系统很多IO操作需要管理身份,所以很有必要在运行前自检.
    '''
    if __windll.shell32.IsUserAnAdmin() == 0:
        return False
    else:
        return True