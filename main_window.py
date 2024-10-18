from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from utils import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # 在这里加载和设置图像
        logo_pixmap = QPixmap(resource_path("assets/images/logo.png"))
        # ... 使用 logo_pixmap
        
        # 初始化其他 UI 元素
