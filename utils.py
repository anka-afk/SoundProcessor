import os
import sys

def resource_path(relative_path):
    """
    获取资源文件的绝对路径，适用于开发和 PyInstaller 打包后的外部资源。
    """
    if getattr(sys, 'frozen', False):  # 如果是打包后的 exe
        base_path = os.path.dirname(sys.executable)  # exe 所在目录
    else:
        base_path = os.path.abspath(".")  # 开发模式，当前目录

    return os.path.join(base_path, relative_path)

