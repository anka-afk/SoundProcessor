from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QFormLayout, QComboBox
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from utils import resource_path
import json
import os
import sys

class InfoFormWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.player = None
        self.audio_output = None

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        title = QLabel("个人信息")
        title.setObjectName("form-title")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(50, 0, 50, 0)
        form_layout.setSpacing(20)
        
        self.name_input = QLineEdit()
        self.name_input.setObjectName("input-field")
        self.name_input.setPlaceholderText("请输入您的姓名")
        form_layout.addRow("姓名:", self.name_input)
        
        self.age_input = QLineEdit()
        self.age_input.setObjectName("input-field")
        self.age_input.setPlaceholderText("请输入您的年龄")
        form_layout.addRow("年龄:", self.age_input)
        
        # 添加性别选择
        self.gender_input = QComboBox()
        self.gender_input.setObjectName("input-field")
        self.gender_input.addItems(["男", "女"])
        form_layout.addRow("性别:", self.gender_input)
        
        self.note_input = QTextEdit()
        self.note_input.setObjectName("input-field")
        self.note_input.setPlaceholderText("请输入备注信息（可选）")
        form_layout.addRow("备注:", self.note_input)
        
        layout.addLayout(form_layout)
        
        submit_button = QPushButton("提交并开始测试")
        submit_button.setObjectName("submit-button")
        submit_button.clicked.connect(self.submitInfo)
        submit_button.setFixedWidth(200)
        
        layout.addStretch()
        layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
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
            self.player.setSource(QUrl.fromLocalFile(resource_path("assets/music/music2.mp3")))
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

    def submitInfo(self):
        name = self.name_input.text()
        age = self.age_input.text()
        gender = self.gender_input.currentText()
        note = self.note_input.toPlainText()
        
        if not name or not age:
            QMessageBox.warning(self, "警告", "姓名和年龄不能为空！")
            return
        
        # 保存用户信息到文件
        user_info = {
            "name": name,
            "age": age,
            "gender": gender,
            "note": note
        }
        self.save_user_info(user_info)
        
        if self.player:
            self.player.stop()
        # 直接跳转到题目页面
        main_window = self.window()
        if hasattr(main_window, 'showQuestionWindow'):
            main_window.showQuestionWindow()
        else:
            print("主窗口没有 showQuestionWindow 方法")

    def save_user_info(self, user_info):
        if getattr(sys, 'frozen', False):
            # 如果是打包后的 exe 运行
            base_path = os.path.dirname(sys.executable)
        else:
            # 如果是在开发环境运行
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(base_path, "user_info.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_info, f, ensure_ascii=False, indent=4)
            print(f"用户信息已保存到: {file_path}")
        except Exception as e:
            print(f"保存用户信息时出错: {e}")

def load_global_pixmap():
    return QPixmap(resource_path("path/to/image.png"))

# 在需要使用时调用
# pixmap = load_global_pixmap()
