import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar, QFrame, QGridLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QPixmap
from audio_handler import AudioHandler
from answer_checker import AnswerChecker
from logger_handler import setup_logger
import pyqtgraph as pg
import numpy as np
from utils import resource_path  # 如果您将函数放在了 utils.py 中
import wave

logger = setup_logger()

# 资源路径
VIDEO_1_PATH = resource_path(os.path.join("assets", "videos", "video1.mp4"))
VIDEO_2_PATH = resource_path(os.path.join("assets", "videos", "video2.mp4"))
HINT_1_PATH = resource_path(os.path.join("assets", "audio", "hint1.mp3"))
HINT_2_PATH = resource_path(os.path.join("assets", "audio", "hint2.mp3"))

class VideoInteractionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.audio_handler = AudioHandler()
        logger.debug("VideoInteractionWindow: AudioHandler 已初始化")
        self.check_audio_devices()
        self.initUI()
        self.reset_state()

    def check_audio_devices(self):
        logger.debug("检查音频设备:")
        for i in range(self.audio_handler.p.get_device_count()):
            dev_info = self.audio_handler.p.get_device_info_by_index(i)
            logger.debug(f"设备 {i}: {dev_info['name']}, 输入通道: {dev_info['maxInputChannels']}")

    def initUI(self):
        # 使用QGridLayout替代QVBoxLayout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除布局边距

        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)  # 设置最小尺寸
        layout.addWidget(self.video_widget, 0, 0, -1, -1)  # 视频小部件占据整个网格

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # 创建一个透明的覆盖层来放置其他控件
        overlay = QWidget(self)
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        overlay_layout = QVBoxLayout(overlay)

        self.status_label = QLabel("准备播放视频")
        self.status_label.setStyleSheet("color: white; font-size: 18px;")
        overlay_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        overlay_layout.addWidget(self.progress_bar)

        self.record_button = QPushButton("点击开始")
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_recording)
        self.record_button.setVisible(False)
        overlay_layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("下一步")
        self.next_button.clicked.connect(self.on_next_clicked)
        self.next_button.setVisible(False)
        overlay_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 频谱图
        self.spectrum_plot = pg.PlotWidget()
        self.spectrum_plot.setBackground('w')
        self.spectrum_curve = self.spectrum_plot.plot(pen='b')
        overlay_layout.addWidget(self.spectrum_plot)

        layout.addWidget(overlay, 0, 0, -1, -1)  # 覆盖层也占据整个网格

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

        self.setLayout(layout)

    def reset_state(self):
        self.current_video = 1
        self.is_recording = False
        self.frames = []
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self.stop_recording)
        logger.debug("VideoInteractionWindow: 状态已重置")

    def showEvent(self, event):
        super().showEvent(event)
        self.reset_state()  # 每次显示窗口时重置状态
        QTimer.singleShot(100, self.play_video)

    def play_video(self):
        video_path = VIDEO_1_PATH if self.current_video == 1 else VIDEO_2_PATH
        if not os.path.exists(video_path):
            QMessageBox.warning(self, "错误", f"视频文件不存在: {video_path}")
            return

        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()
        logger.debug(f"正在播放视频: {video_path}")

        # 在视频播放 5 秒后开始录音
        QTimer.singleShot(5000, self.prepare_recording)

    def prepare_recording(self):
        logger.debug("VideoInteractionWindow: 准备录音")
        self.media_player.pause()
        self.status_label.setText("准备录音...")
        self.record_button.setVisible(True)
        QTimer.singleShot(500, self.start_recording)  # 给音频设备一些时间来准备

    def start_recording(self):
        self.audio_handler.start_recording()
        self.is_recording = True
        self.record_button.setText("正在录音...")
        self.record_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        logger.debug("VideoInteractionWindow: 开始录音")
        
        # 设置录音时间为5秒
        self.recording_timer.start(5000)
        self.start_progress_timer()

    def start_progress_timer(self):
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(50)  # 每50毫秒更新一次进度条

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.progress_timer.stop()

    def update_plot(self):
        if self.is_recording:
            data = self.audio_handler.record()
            spectrum = np.abs(np.fft.fft(data))
            spectrum = np.log10(spectrum[:len(spectrum)//2] + 1e-10)
            self.spectrum_curve.setData(spectrum)

    def stop_recording(self):
        if self.is_recording:
            logger.debug("VideoInteractionWindow: 尝试停止录音")
            try:
                recognized_text, audio_data = self.audio_handler.stop_recording()
                self.is_recording = False
                self.record_button.setText("点击开始")
                self.record_button.setEnabled(True)
                self.progress_bar.setVisible(False)
                self.recording_timer.stop()
                self.progress_timer.stop()
                logger.debug(f"VideoInteractionWindow: 录音成功停止，识别的文本: {recognized_text}")
                
                # 如果是第二个视频，保存录音结果
                if self.current_video == 2:
                    self.save_audio(audio_data)
            except Exception as e:
                logger.error(f"VideoInteractionWindow: 停止录音时出错 - {str(e)}")
                recognized_text = ""
            
            if recognized_text:
                self.status_label.setText("录音完成，已检测到回答")
                logger.debug(f"检测到回答: {recognized_text}")
                if self.current_video == 1:
                    self.current_video = 2
                    QTimer.singleShot(1000, self.play_video)  # 延迟1秒后播放下一个视频
                else:
                    self.check_answer(recognized_text)
            else:
                self.status_label.setText("未检测到回答，请重新尝试")
                logger.warning("未检测到回答")
                QTimer.singleShot(2000, self.play_video)  # 2秒后重新播放视频

    def save_audio(self, audio_data):
        output_filename = "output.wav"
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(16000)  # 假设采样率为16kHz，根据实际情况调整
        wf.writeframes(audio_data)
        wf.close()
        logger.debug(f"录音已保存为 {output_filename}")

    def check_answer(self, recognized_text):
        is_correct = AnswerChecker.check_answer(recognized_text, "杯子")
        if is_correct:
            self.play_hint(HINT_1_PATH)
            self.status_label.setText("回答正确！")
            self.main_window.show_audio_processing_window()
            self.reset_state()  # 在退出视频交互页面时重置状态
        else:
            self.play_hint(HINT_2_PATH)
            self.status_label.setText(f"回答错误。您的回答是：{recognized_text}")
            QTimer.singleShot(2000, self.play_video)
        self.next_button.setVisible(True)

    def play_hint(self, hint_path):
        if not os.path.exists(hint_path):
            QMessageBox.warning(self, "错误", f"提示音频文件不存在: {hint_path}")
            return

        self.media_player.setSource(QUrl.fromLocalFile(hint_path))
        self.media_player.play()

    def on_next_clicked(self):
        self.main_window.show_audio_processing_window()
        self.reset_state()  # 在退出视频交互页面时重置状态
