from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtCore import Qt
from audio_processing import load_audio, compute_energy, compute_avg_energy, extract_f0, extract_formants, determine_tone
import pandas as pd
import numpy as np
import os

class AudioProcessingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.process_audio()

    def initUI(self):
        layout = QVBoxLayout()

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def process_audio(self):
        file_path = "output.wav"
        if os.path.exists(file_path):
            results = self.process_audio_file(file_path)
            self.display_results(results)
            self.status_label.setText("处理完成")
        else:
            self.status_label.setText("错误: output.wav 文件不存在")

    def process_audio_file(self, filepath):
        y, sr = load_audio(filepath)
        
        energy = compute_energy(y)
        avg_energy = compute_avg_energy(energy)
        
        duration = len(y) / sr
        timestamps = np.arange(0, duration, 0.01)
        
        segments = []
        for i in range(1, len(energy)):
            if energy[i] > avg_energy * 1.08:
                start = timestamps[i]
                end = start + 0.05
                if 0.05 <= end - start <= 0.8:
                    segments.append((start, end))
        
        results = []
        for segment in segments:
            start, end = segment
            seg_duration = end - start
            
            start_30 = start + 0.3 * seg_duration
            end_80 = start + 0.8 * seg_duration
            
            f0_mean = extract_f0(y, sr, start_30, end_80)
            f1_mean, f2_mean = extract_formants(y, sr, start_30, end_80)
            
            start_20 = start_30 - 0.2 * seg_duration
            end_20 = end_80 + 0.2 * seg_duration
            d0_a2 = extract_f0(y, sr, start_20, start_30)
            f0_a3 = extract_f0(y, sr, end_80, end_20)
            
            tone = determine_tone(f0_mean, d0_a2, f0_a3)
            
            results.append([f0_mean, f1_mean, f2_mean, tone, avg_energy])
        
        return results

    def display_results(self, results):
        df = pd.DataFrame(results, columns=["F0均值", "F1均值", "F2均值", "声调", "平均能量"])
        
        self.result_table.setRowCount(len(df))
        self.result_table.setColumnCount(len(df.columns))
        self.result_table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 使单元格不可编辑
                self.result_table.setItem(i, j, item)

        self.result_table.resizeColumnsToContents()
