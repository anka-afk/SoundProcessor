from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from utils import resource_path  # 如果您将函数放在了 utils.py 中

class WelcomeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # 添加logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("assets/images/logo.png"))
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            print("Failed to load logo image")
        layout.addWidget(logo_label)
        
        title = QLabel("语音分析识别系统")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("欢迎使用我们的语音识别系统")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Microsoft YaHei", 18))
        subtitle.setStyleSheet("color: #666666;")
        
        start_button = QPushButton("开始测试")
        start_button.setObjectName("start-button")
        start_button.clicked.connect(self.parent().showInfoForm)
        start_button.setFixedWidth(200)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
