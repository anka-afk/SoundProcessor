from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QTextBrowser, QFrame, QMessageBox
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import pyqtgraph as pg
import numpy as np
from audio_handler import AudioHandler
from answer_checker import AnswerChecker
from logger_handler import setup_logger
from utils import resource_path  # 如果您将函数放在了 utils.py 中

logger = setup_logger()

class QuestionWindow(QWidget):
    answer_correct = pyqtSignal()

    def __init__(self, main_window, question_data=None, question_number=None):
        super().__init__()
        self.main_window = main_window
        self.question_data = question_data or {}
        self.question_number = question_number
        self.audio_handler = AudioHandler()
        self.is_recording = False
        self.frames = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        if self.question_number is not None:
            number_label = QLabel(f"第 {self.question_number + 1} 题")
            layout.addWidget(number_label, alignment=Qt.AlignmentFlag.AlignCenter)

        title = QLabel(self.question_data.get('title', ''))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        content = QTextBrowser()
        content.setPlainText(self.question_data.get('content', ''))
        layout.addWidget(content)

        # 显示图片（如果有）
        media_path = self.question_data.get('media', '')
        if isinstance(media_path, str) and media_path.endswith(('.png', '.jpg', '.jpeg')):
            image_label = QLabel()
            pixmap = QPixmap(resource_path(media_path))
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
            else:
                print(f"Failed to load image: {media_path}")

        # 录音按钮
        self.record_button = QPushButton("按住说话")
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_recording)
        layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 频谱图
        spectrum_frame = QFrame()
        spectrum_layout = QVBoxLayout(spectrum_frame)
        self.spectrum_plot = pg.PlotWidget()
        self.spectrum_plot.setBackground('w')
        self.spectrum_curve = self.spectrum_plot.plot(pen='b')
        spectrum_layout.addWidget(self.spectrum_plot)
        layout.addWidget(spectrum_frame)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

    def start_recording(self):
        self.audio_handler.start_recording()
        self.is_recording = True
        self.record_button.setText("松开停止录音")
        logger.debug("开始录音")

    def stop_recording(self):
        if self.is_recording:
            recognized_text = self.audio_handler.stop_recording()
            self.is_recording = False
            self.record_button.setText("按住说话")
            correct_answer = self.question_data.get('answer', '')
            
            logger.debug(f"识别的文本：{recognized_text}")
            logger.debug(f"正确答案：{correct_answer}")
            
            if not recognized_text:
                QMessageBox.warning(self, "警告", "没有识别到语音，请重新录音。")
            else:
                is_correct = AnswerChecker.check_answer(recognized_text, correct_answer)
                self.main_window.record_result(self.question_number, is_correct, recognized_text, correct_answer)
                if is_correct:
                    self.answer_correct.emit()
                    QMessageBox.information(self, "正确", "回答正确！")
                    self.main_window.show_next_question()
                else:
                    QMessageBox.warning(self, "错误", "回答错误，请重试。")

    def update_plot(self):
        if self.is_recording:
            data = self.audio_handler.record()
            spectrum = np.abs(np.fft.fft(data))
            spectrum = np.log10(spectrum[:len(spectrum)//2] + 1e-10)
            self.spectrum_curve.setData(spectrum)

def load_global_pixmap():
    return QPixmap(resource_path("path/to/image.png"))

# 删除这一行
# logo_pixmap = QPixmap(resource_path("assets/images/logo.png"))
