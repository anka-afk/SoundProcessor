from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from utils import resource_path  # 如果您将函数放在了 utils.py 中

class WelcomeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.player = None
        self.audio_output = None

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
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

    def showEvent(self, event):
        super().showEvent(event)
        self.initAudio()

    def initAudio(self):
        if self.player is None:
            self.player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(QUrl.fromLocalFile(resource_path("assets/music/music1.mp3")))
            self.audio_output.setVolume(0.5)  # 设置音量为 50%
        self.player.play()

    def hideEvent(self, event):
        if self.player:
            self.player.stop()
        super().hideEvent(event)

    def closeEvent(self, event):
        if self.player:
            self.player.stop()
        super().closeEvent(event)
