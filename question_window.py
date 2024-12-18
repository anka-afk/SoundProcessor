from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QTextBrowser, QFrame, QMessageBox
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QTimer, pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QPixmap,QKeyEvent
import pyqtgraph as pg
import numpy as np
from audio_handler import AudioHandler
from answer_checker import AnswerChecker
from logger_handler import setup_logger
from utils import resource_path
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

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

        # 初始化音频播放器
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

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

        self.load_media(layout)
        # 设置焦点，以便捕获键盘事件
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event: QKeyEvent):
        """捕获键盘输入事件"""
        if event.key() == Qt.Key.Key_1:  # 小键盘1跳转到下一题
            print("Debug: 跳转到下一题")
            self.main_window.show_next_question()
        elif event.key() == Qt.Key.Key_2:  # 小键盘2返回上一题
            print("Debug: 返回上一题")
            self.main_window.show_previous_question()
        else:
            super().keyPressEvent(event)  # 调用父类处理其他按键

    def start_recording(self):
        self.audio_handler.start_recording()
        self.is_recording = True
        self.record_button.setText("松开停止录音")
        logger.debug("开始录音")

    def stop_recording(self):
        if self.is_recording:
            recognized_text, audio_data = self.audio_handler.stop_recording()
            self.is_recording = False
            self.record_button.setText("按住说话")
            correct_answer = self.question_data.get('answer', None)  # 获取答案字段

            logger.debug(f"识别的文本：{recognized_text}")
            logger.debug(f"正确答案：{correct_answer}")

            if not recognized_text:
                # 如果录音内容为空
                QMessageBox.warning(self, "警告", "没有识别到语音，请重新录音。")
            else:
                if correct_answer:  # 如果存在答案字段，验证答案
                    is_correct = AnswerChecker.check_answer(recognized_text, correct_answer)
                else:  # 如果不存在答案字段，只检查录音是否非空
                    is_correct = True  # 录音内容不为空即为正确

                # 记录结果
                self.main_window.record_result(self.question_number, is_correct, recognized_text, correct_answer or "N/A")

                if is_correct:
                    # 保存录音文件到结果文件夹
                    # 获取用户名
                    if hasattr(self.main_window, "user_info"):
                        user_name = self.main_window.user_info.get("name", "Unknown_User")
                    else:
                        user_name = "Unknown_User"
                    self.save_recording(user_name, self.question_number, audio_data)
                    
                    self.answer_correct.emit()
                    self.play_audio("assets/audio/hint1.mp3")  # 播放正确提示音
                    QMessageBox.information(self, "提示", "回答成功！")
                    self.main_window.show_next_question()
                else:
                    self.play_audio("assets/audio/hint2.mp3")  # 播放错误提示音
                    QMessageBox.warning(self, "错误", "回答错误，请重试。")

    def save_recording(self, user_name, question_number, audio_data):
        """保存录音文件到结果文件夹"""
        base_path = os.path.join(os.getcwd(), "结果", user_name)
        os.makedirs(base_path, exist_ok=True)  # 确保用户目录存在

        file_path = os.path.join(base_path, f"recording_question_{question_number}.wav")
        try:
            with open(file_path, "wb") as f:
                f.write(audio_data)
            print(f"录音文件已保存到: {file_path}")
            logger.debug(f"录音文件已保存到: {file_path}")
        except Exception as e:
            logger.error(f"保存录音文件时出错: {e}")

    def update_plot(self):
        if self.is_recording:
            data = self.audio_handler.record()
            spectrum = np.abs(np.fft.fft(data))
            spectrum = np.log10(spectrum[:len(spectrum)//2] + 1e-10)
            self.spectrum_curve.setData(spectrum)

    def play_audio(self, audio_path):
        self.media_player.setSource(QUrl.fromLocalFile(resource_path(audio_path)))
        self.media_player.play()

    def closeEvent(self, event):
        """释放媒体播放器和其他资源"""
        if hasattr(self, "media_player") and self.media_player is not None:
            self.media_player.stop()
            self.media_player.setSource(QUrl())  # 清空媒体源
            self.media_player = None
        event.accept()

    def add_recording_controls(self,layout):
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
        
    def load_media(self, layout):
        """加载媒体或执行步骤"""
        if "steps" in self.question_data:
            self.steps = self.question_data["steps"]
            self.current_step_index = 0
            self.layout = layout  # 保存布局引用
            self.execute_next_step()
        else:
            # 如果没有 steps，执行默认的媒体加载
            self.load_default_media(layout)
            
    def load_default_media(self, layout):
        """默认的媒体加载逻辑"""
        media = self.question_data.get("media", {})
        media_type = media.get("type")

        if media_type == "image":
            image_path = resource_path(media["path"])
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
                layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        elif media_type == "video":
            self.video_widget = QVideoWidget(self)
            self.media_player = QMediaPlayer(self)
            self.media_player.setVideoOutput(self.video_widget)
            self.media_player.setSource(QUrl.fromLocalFile(resource_path(media["path"])))
            layout.addWidget(self.video_widget)
            self.media_player.play()

        # 添加录音控件
        interaction_type = self.question_data.get("interaction", "record")
        if interaction_type == "record":
            self.add_recording_controls(layout)
            
    def execute_next_step(self):
        """执行 steps 中的下一步"""
        if self.current_step_index >= len(self.steps):
            print("所有步骤已执行完毕")
            return

        step = self.steps[self.current_step_index]
        action = step.get("action")

        if action == "wait":
            duration = step.get("duration", 1) * 1000  # 转换为毫秒
            print(f"等待 {duration / 1000} 秒...")
            QTimer.singleShot(duration, self.execute_next_step)

        elif action == "play_audio":
            audio_path = resource_path(step.get("path", ""))
            print(f"播放音频: {audio_path}")

            if not hasattr(self, "media_player"):
                self.media_player = QMediaPlayer(self)
                self.audio_output = QAudioOutput(self)
                self.media_player.setAudioOutput(self.audio_output)
            
            self.media_player.setSource(QUrl.fromLocalFile(audio_path))
            self.media_player.play()

            self.media_player.mediaStatusChanged.connect(
                lambda status: self.execute_next_step() 
                if status == QMediaPlayer.MediaStatus.EndOfMedia else None
            )

        elif action == "record":
            record_type = step.get("type", "manual")
            duration = step.get("duration", 5) * 1000  # 自动录音的时长

            if record_type == "manual":
                print("自行录音：显示录音按钮")
                if not hasattr(self, "record_button"):
                    self.add_recording_controls(self.layout)
            elif record_type == "auto":
                print("自动录音：倒数 3 秒开始录音")
                self.auto_recording(duration)

        elif action == "show_hint":
            hint = step.get("hint", "")
            QMessageBox.information(self, "提示", hint)
            self.execute_next_step()

        self.current_step_index += 1

    def auto_recording(self, duration):
        """自动录音：倒数 3 秒后自动开始录音，指定时长后停止"""
        countdown_label = QLabel("录音倒计时：3 秒")
        countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(countdown_label)

        def update_countdown(seconds_left):
            countdown_label.setText(f"录音倒计时：{seconds_left} 秒")
            if seconds_left == 0:
                countdown_label.setText("录音中...")
                self.start_recording()
                QTimer.singleShot(duration, self.stop_recording_and_continue)

        # 使用倒计时逐步更新文本
        for i in range(3, -1, -1):
            QTimer.singleShot((3 - i) * 1000, lambda seconds=i: update_countdown(seconds))


    def stop_recording_and_continue(self):
        """停止录音并继续执行步骤"""
        self.stop_recording()
        self.execute_next_step()