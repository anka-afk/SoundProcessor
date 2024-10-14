import pyaudio
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QMessageBox, QTextEdit, QFrame, QTextBrowser)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
import pyqtgraph as pg
from vosk import Model, KaldiRecognizer
import json
import os
import difflib
import traceback
import sys
import logging
import pypinyin
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl

# 设置日志
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionPage(QWidget):
    answer_correct = pyqtSignal()  # 定义新的信号

    def __init__(self, main_window, question_data=None, question_number=None):
        super().__init__()
        self.main_window = main_window
        self.question_data = question_data
        self.question_number = question_number
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = np.zeros(4096)
        self.frames = []
        self.max_recording_time = 10  # 最大录音时间（秒）
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.stop_recording)

        try:
            model_path = "vosk-model-small-cn-0.22"
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Vosk模型路径不存在: {model_path}")
            self.model = Model(model_path)
            self.rec = KaldiRecognizer(self.model, 16000)
            logger.info("Vosk模型初始化成功")
        except Exception as e:
            logger.error(f"初始化Vosk模型时出错: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "错误", f"初始化语音识别模型失败: {str(e)}")

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 题目序号
        if self.question_number is not None:
            number_label = QLabel(f"第 {self.question_number + 1} 题")
            number_label.setObjectName("question-number")
            layout.addWidget(number_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # 题目标题
        title = QLabel(self.question_data['title'])
        title.setObjectName("question-title")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # 题目内容
        content = QTextBrowser()
        content.setObjectName("question-content")
        content.setPlainText(self.question_data['content'])
        content.setReadOnly(True)
        content.setOpenExternalLinks(True)
        layout.addWidget(content)

        # 媒体显示
        media_layout = QHBoxLayout()
        media_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if isinstance(self.question_data['media'], list):
            for media in self.question_data['media']:
                if isinstance(media, str):
                    if media.lower().endswith(('.mp4', '.avi', '.mov')):  # 视频文件
                        self.video_widget = QVideoWidget()
                        self.media_player = QMediaPlayer()
                        self.media_player.setVideoOutput(self.video_widget)
                        self.media_player.setSource(QUrl.fromLocalFile(media))
                        media_layout.addWidget(self.video_widget)
                        
                        # 添加播放/暂停按钮
                        self.play_button = QPushButton("播放/暂停")
                        self.play_button.clicked.connect(self.play_pause_video)
                        media_layout.addWidget(self.play_button)
                    else:  # 图片文件
                        image = QLabel()
                        pixmap = QPixmap(media)
                        if not pixmap.isNull():
                            image.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                        media_layout.addWidget(image)
                elif isinstance(media, dict) and media.get('type') == 'video':
                    self.video_widget = QVideoWidget()
                    self.media_player = QMediaPlayer()
                    self.media_player.setVideoOutput(self.video_widget)
                    self.media_player.setSource(QUrl.fromLocalFile(media['source']))
                    media_layout.addWidget(self.video_widget)
                    
                    # 添加播放/暂停按钮
                    self.play_button = QPushButton("播放/暂停")
                    self.play_button.clicked.connect(self.play_pause_video)
                    media_layout.addWidget(self.play_button)
                elif isinstance(media, dict) and media.get('type') == 'image':
                    image = QLabel()
                    pixmap = QPixmap(media['source'])
                    if not pixmap.isNull():
                        image.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                    media_layout.addWidget(image)
        elif isinstance(self.question_data['media'], str):
            if self.question_data['media'].lower().endswith(('.mp4', '.avi', '.mov')):  # 视频文件
                self.video_widget = QVideoWidget()
                self.media_player = QMediaPlayer()
                self.media_player.setVideoOutput(self.video_widget)
                self.media_player.setSource(QUrl.fromLocalFile(self.question_data['media']))
                media_layout.addWidget(self.video_widget)
                
                # 添加播放/暂停按钮
                self.play_button = QPushButton("播放/暂停")
                self.play_button.clicked.connect(self.play_pause_video)
                media_layout.addWidget(self.play_button)
            else:  # 图片文件
                image = QLabel()
                pixmap = QPixmap(self.question_data['media'])
                if not pixmap.isNull():
                    image.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                media_layout.addWidget(image)

        layout.addLayout(media_layout)

        # 录音按钮
        self.record_button = QPushButton("按住说话")
        self.record_button.setObjectName("record-button")
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_recording)
        self.record_button.setFixedWidth(200)
        layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 频谱图
        spectrum_frame = QFrame()
        spectrum_frame.setObjectName("spectrum-frame")
        spectrum_layout = QVBoxLayout(spectrum_frame)
        self.spectrum_plot = pg.PlotWidget()
        self.spectrum_plot.setBackground('w')
        self.spectrum_curve = self.spectrum_plot.plot(pen='b')
        self.spectrum_plot.setFixedHeight(100)
        spectrum_layout.addWidget(self.spectrum_plot)
        layout.addWidget(spectrum_frame)

        # 提示
        hint = QTextBrowser()
        hint.setObjectName("question-hint")
        hint.setPlainText(self.question_data['hint'])
        hint.setReadOnly(True)
        hint.setOpenExternalLinks(True)
        layout.addWidget(hint)

        # 调试输出
        debug_label = QLabel("调试输出:")
        debug_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(debug_label)
        self.debug_output = QTextEdit(self)
        self.debug_output.setReadOnly(True)
        self.debug_output.setObjectName("debug-output")
        self.debug_output.setFixedHeight(100)
        layout.addWidget(self.debug_output)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # 定时器用于更新频谱图
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

        logger.info("UI初始化完成")

    def start_recording(self):
        try:
            logger.info("开始录音")
            self.is_recording = True
            self.frames = []
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=16000,
                                          input=True,
                                          frames_per_buffer=4096,
                                          stream_callback=self.audio_callback)
            self.stream.start_stream()
            self.log("开始录音")
            self.recording_timer.start(self.max_recording_time * 1000)  # 启动录音计时器
        except Exception as e:
            logger.error(f"开始录音时出错: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "错误", f"开始录音失败: {str(e)}")

    def stop_recording(self):
        try:
            logger.info("停止录音")
            self.recording_timer.stop()  # 停止录音计时器
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            self.is_recording = False
            self.log("停止录音")
            self.process_audio()
        except Exception as e:
            logger.error(f"停止录音时出错: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "错误", f"停止录音失败: {str(e)}")

    def audio_callback(self, in_data, frame_count, time_info, status):
        try:
            if status:
                logger.warning(f"音频回调状态: {status}")
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.data = audio_data
            self.frames.append(in_data)
            volume = np.abs(audio_data).mean()
            logger.debug(f"接收到音频数据，大小：{len(in_data)} 字节，音量：{volume}")
            return (audio_data, pyaudio.paContinue)
        except Exception as e:
            logger.error(f"音频回调函数出错: {str(e)}", exc_info=True)
            return (in_data, pyaudio.paAbort)

    def update_plot(self):
        try:
            if self.is_recording:
                spectrum = np.abs(np.fft.fft(self.data))
                spectrum = spectrum[:len(spectrum)//2]
                spectrum = np.log10(spectrum + 1e-10)
                self.spectrum_curve.setData(spectrum)
        except Exception as e:
            logger.error(f"更新频谱图时出错: {str(e)}", exc_info=True)

    def process_audio(self):
        try:
            if not self.frames:
                logger.warning("没有录到音频数据")
                QMessageBox.warning(self, "警告", "没有录到音频数据，请重新录音。")
                return

            audio_data = b''.join(self.frames)
            logger.info(f"音频数据大小: {len(audio_data)} 字节")

            # 使用流式处理方法
            self.rec.Reset()  # 重置识别器
            recognized_text = ""
            for chunk in self.frames:
                if self.rec.AcceptWaveform(chunk):
                    result = json.loads(self.rec.Result())
                    logger.debug(f"中间识别结果: {result}")
                    recognized_text += result.get('text', '') + " "
            
            # 处理最后的结果
            final_result = json.loads(self.rec.FinalResult())
            logger.info(f"最终识别结果: {final_result}")
            recognized_text += final_result.get('text', '')

            if recognized_text:
                # 移除多余的空格
                recognized_text = ' '.join(recognized_text.split())
                # 将常见的语气词替换为更可能的答案
                recognized_text = recognized_text.replace("诶", "欸").replace("诶", "唉")
                logger.info(f"处理后的识别结果: {recognized_text}")
                self.check_answer(recognized_text)
            else:
                logger.warning("无法识别语音")
                QMessageBox.warning(self, "警告", "无法识别语音，请重新录音。")
        except Exception as e:
            logger.error(f"处理音频时出错: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "错误", f"处理音频失败: {str(e)}")

    def check_answer(self, recognized_text):
        try:
            correct_answer = self.question_data['answer']
            logger.info(f"正确答案: {correct_answer}")
            logger.info(f"用户回答: {recognized_text}")
            
            # 将识别文本和正确答案转换为拼音
            recognized_pinyin = ''.join(pypinyin.lazy_pinyin(recognized_text))
            correct_pinyin = ''.join(pypinyin.lazy_pinyin(correct_answer))
            
            logger.info(f"识别文本拼音: {recognized_pinyin}")
            logger.info(f"正确答案拼音: {correct_pinyin}")
            
            # 计算拼音的相似度
            similarity = difflib.SequenceMatcher(None, recognized_pinyin, correct_pinyin).ratio()
            
            logger.info(f"拼音相似度: {similarity}")

            if similarity >= 0.9:  # 提高阈值，因为我们现在比较的是拼音
                logger.info("回答正确")
                QMessageBox.information(self, "正确", "回答正确！可以进入下一题。")
                self.answer_correct.emit()  # 发出信号
            elif similarity >= 0.75:  # 降低阈值
                logger.info("回答接近正确")
                QMessageBox.warning(self, "接近正确", f"您的回答接近正确。\n您的回答是：{recognized_text}\n正确答案是：{correct_answer}\n请再试一次。")
            else:
                logger.info("回答错误")
                QMessageBox.warning(self, "错误", f"回答不正确。\n您的回答是：{recognized_text}\n正确答案是：{correct_answer}\n请重新录音。")
        except Exception as e:
            logger.error(f"检查答案时出错: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "错误", f"检查答案失败: {str(e)}")

    def log(self, message):
        try:
            self.debug_output.append(message)
            print(message)
            self.debug_output.ensureCursorVisible()
        except Exception as e:
            logger.error(f"日志记录失败: {str(e)}", exc_info=True)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'media_player'):
                self.media_player.stop()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            self.audio.terminate()
            event.accept()
        except Exception as e:
            logger.error(f"关闭事件处理失败: {str(e)}", exc_info=True)
            event.accept()

    def play_pause_video(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

def exception_hook(exctype, value, traceback):
    error_msg = f"Uncaught exception: {exctype.__name__}: {value}"
    logger.critical(error_msg, exc_info=True)
    print(error_msg)
    print("Traceback:")
    print("".join(traceback.format_tb(traceback)))
    QMessageBox.critical(None, "错误", f"发生未捕获的异常: {exctype.__name__}: {value}\n\n请查看日志文件以获取详细信息。")

sys.excepthook = exception_hook
