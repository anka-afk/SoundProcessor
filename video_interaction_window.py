import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt, QTimer
from audio_handler import AudioHandler
from answer_checker import AnswerChecker
from logger_handler import setup_logger

logger = setup_logger()

# 资源路径
VIDEO_1_PATH = os.path.join("assets", "videos", "video1.mp4")
VIDEO_2_PATH = os.path.join("assets", "videos", "video2.mp4")
HINT_1_PATH = os.path.join("assets", "audio", "hint1.mp3")
HINT_2_PATH = os.path.join("assets", "audio", "hint2.mp3")

class VideoInteractionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.audio_handler = AudioHandler()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)  # 设置最小尺寸
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        self.status_label = QLabel("准备播放视频")
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("下一步")
        self.next_button.clicked.connect(self.on_next_clicked)
        self.next_button.setVisible(False)
        layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.current_video = 1
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self.play_video)

    def play_video(self):
        video_path = VIDEO_1_PATH if self.current_video == 1 else VIDEO_2_PATH
        if not os.path.exists(video_path):
            QMessageBox.warning(self, "错误", f"视频文件不存在: {video_path}")
            return

        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()
        logger.debug(f"正在播放视频: {video_path}")

        # 设置一个定时器，在视频播放4秒后开始录音
        QTimer.singleShot(4000, self.start_recording)

    def start_recording(self):
        self.status_label.setText("正在录音...")
        self.audio_handler.start_recording()
        QTimer.singleShot(3000, self.stop_recording)

    def stop_recording(self):
        recognized_text = self.audio_handler.stop_recording()
        if recognized_text:
            self.status_label.setText("录音完成，已检测到回答")
            if self.current_video == 1:
                self.current_video = 2
                self.play_video()
            else:
                self.check_answer(recognized_text)
        else:
            self.status_label.setText("未检测到回答，请重新尝试")
            self.play_video()

    def check_answer(self, recognized_text):
        is_correct = AnswerChecker.check_answer(recognized_text, "杯子")
        if is_correct:
            self.play_hint(HINT_1_PATH)
            self.status_label.setText("回答正确！")
        else:
            self.play_hint(HINT_2_PATH)
            self.status_label.setText(f"回答错误。您的回答是：{recognized_text}")
        self.next_button.setVisible(True)

    def play_hint(self, hint_path):
        if not os.path.exists(hint_path):
            QMessageBox.warning(self, "错误", f"提示音频文件不存在: {hint_path}")
            return

        self.media_player.setSource(QUrl.fromLocalFile(hint_path))
        self.media_player.play()

    def on_next_clicked(self):
        self.main_window.show_summary_window()
