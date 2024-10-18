import json
import pyaudio
import wave
import numpy as np
from vosk import Model, KaldiRecognizer
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AudioHandler:
    def __init__(self):
        model_path = resource_path('vosk-model-small-cn-0.22')
        print(f"Attempting to load model from: {model_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"_MEIPASS: {getattr(sys, '_MEIPASS', 'Not found')}")
        print(f"Files in current directory: {os.listdir()}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        
        print(f"Files in model directory: {os.listdir(model_path)}")
        
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.frames = []
        self.sample_rate = 16000
        self.chunk = 1024
        
        # 初始化Vosk模型
        self.model = Model(model_path)
        self.rec = None
        logger.debug("Vosk模型已初始化")

        # 检查可用的录音设备
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                logger.debug(f"Input Device id {i} - {self.p.get_device_info_by_host_api_device_index(0, i).get('name')}")

    def start_recording(self):
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
            self.is_recording = True
            self.frames = []
            self.rec = KaldiRecognizer(self.model, self.sample_rate)
            logger.debug("开始录音")
        except Exception as e:
            logger.error(f"开始录音时发生错误: {str(e)}")
            self.is_recording = False

    def stop_recording(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.is_recording = False
        
        audio_data = b''.join(self.frames)
        logger.debug(f"录音结束，数据长度：{len(audio_data)} 字节")
        
        if self.rec.AcceptWaveform(audio_data):
            result = json.loads(self.rec.Result())
        else:
            result = json.loads(self.rec.FinalResult())
        
        recognized_text = result.get('text', '')
        logger.debug(f"识别的文本：{recognized_text}")
        return recognized_text

    def record(self):
        if self.is_recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
                return np.frombuffer(data, dtype=np.int16)
            except Exception as e:
                logger.error(f"录音过程中发生错误: {str(e)}")
                self.is_recording = False
        return np.zeros(self.chunk)
