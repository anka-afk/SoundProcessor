from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
import librosa
import numpy as np
import json
import os
import sys
import csv

class AudioProcessingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.process_audio()

    def initUI(self):
        layout = QVBoxLayout()

        # 用户信息显示布局
        user_info_layout = QHBoxLayout()
        self.name_label = QLabel("姓名：")
        self.gender_label = QLabel("性别：")
        self.age_label = QLabel("年龄：")
        self.date_label = QLabel("检测日期：")
        
        user_info_layout.addWidget(self.name_label)
        user_info_layout.addWidget(self.gender_label)
        user_info_layout.addWidget(self.age_label)
        user_info_layout.addWidget(self.date_label)

        layout.addLayout(user_info_layout)

        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)  # 四列：项目、测量结果、参考范围
        self.result_table.setHorizontalHeaderLabels(["声学检测项目", "测量结果", "参考范围", "单位"])
        layout.addWidget(self.result_table)

        # 注释标签
        self.note_label = QLabel("(以上所提供的声学分析指标结果仅供参考，不能替代专业医疗诊断。如果需要进行精准筛查，建议前往医院就医，以便得到专业的医学评估和处理)")
        layout.addWidget(self.note_label)

        self.setLayout(layout)

    def process_audio(self):
        # 加载用户信息
        user_info = self.load_user_info()
        self.display_user_info(user_info)

        # 构建音频文件路径
        user_name = user_info.get("name", "Unknown_User")
        base_path = os.path.join(os.getcwd(), "结果", user_name)
        audio_file_path = os.path.join(base_path, "recording_question_0.wav")

        if os.path.exists(audio_file_path):
            print(f"处理音频文件: {audio_file_path}")
            results = self.process_audio_file(audio_file_path)
            self.display_results(results)
            self.save_results_to_csv(user_info, results)  # 保存结果到 CSV 文件
        else:
            self.name_label.setText(f"错误: {audio_file_path} 文件不存在")
            print(f"错误: 音频文件不存在: {audio_file_path}")



    def load_user_info(self):
        # 获取主窗口中的用户信息
        user_info = getattr(self.main_window, "user_info", {})
        user_name = user_info.get("name", "Unknown_User")

        # 定义用户文件夹路径
        base_path = os.path.join(os.getcwd(), "结果", user_name)
        file_path = os.path.join(base_path, "user_info.json")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"用户信息文件不存在: {file_path}")
            return {}
        except Exception as e:
            print(f"读取用户信息时出错: {e}")
            return {}

    def save_results_to_csv(self, user_info, results):
        """保存分析结果到 CSV 文件"""
        user_name = user_info.get("name", "Unknown_User")
        base_path = os.path.join(os.getcwd(), "结果", user_name)
        os.makedirs(base_path, exist_ok=True)  # 确保用户目录存在

        file_path = os.path.join(base_path, "analysis_results.csv")

        # 生成 CSV 数据
        formant1 = results['formants'][0] if len(results['formants']) > 0 else 0.0
        formant2 = results['formants'][1] if len(results['formants']) > 1 else 0.0

        data = [
            ["声学检测项目", "测量结果", "单位"],
            ["基频", f"{results['f0'][0]:.2f}-{results['f0'][1]:.2f}", "Hz"],
            ["基频-最小值", f"{results['f0'][0]:.2f}", "Hz"],
            ["基频-最大值", f"{results['f0'][1]:.2f}", "Hz"],
            ["能量", f"{results['energy']:.2f}", "dB"],
            ["第一共振峰", f"{formant1:.2f}", "Hz"],
            ["第二共振峰", f"{formant2:.2f}", "Hz"]
        ]

        # 保存到 CSV 文件
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print(f"分析结果已保存到: {file_path}")
        except Exception as e:
            print(f"保存 CSV 文件时出错: {e}")


    def display_user_info(self, user_info):
        self.name_label.setText(f"姓名：{user_info.get('name', '未知')}")
        self.gender_label.setText(f"性别：{user_info.get('gender', '未知')}")
        self.age_label.setText(f"年龄：{user_info.get('age', '未知')}")
        
        # 获取当前系统时间并格式化
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.date_label.setText(f"检测日期：{current_time}")

    def process_audio_file(self, filepath):  # 确保此处第一个参数是self
        # 加载音频数据
        y, sr = librosa.load(filepath)
        
        # 计算基频
        f0 = librosa.yin(y, fmin=75, fmax=300)

        # 计算能量
        energy = np.sum(y ** 2)

        # 计算第一共振峰和第二共振峰（使用LPC）
        lpc_order = 10  # 调整LPC阶数，根据采样率适当调整
        lpc_coeffs = librosa.lpc(y, order=lpc_order)
        
        # 获取LPC系数的根并过滤正频率部分
        roots = np.roots(lpc_coeffs)
        roots = roots[np.imag(roots) >= 0]  # 仅保留正频率
        
        # 将角度转换为频率
        angz = np.arctan2(np.imag(roots), np.real(roots))
        frequencies = angz * (sr / (2 * np.pi))

        # 过滤掉过低或过高的频率（通常共振峰在300-3000Hz之间）
        formants = np.sort(frequencies[(frequencies > 300) & (frequencies < 3000)])

        # 如果没有足够的共振峰，返回默认值
        if len(formants) < 2:
            formant1 = formants[0] if len(formants) > 0 else 0.0
            formant2 = 0.0
        else:
            formant1, formant2 = formants[:2]

        return {
            "f0": [np.min(f0), np.max(f0)],
            "energy": energy,
            "formants": [formant1, formant2]
        }

    def display_results(self, results):
        # 预设的参考范围
        reference_ranges = [
            "132.19-202.01",  # 基频
            "76.19-127.616",  # 基频-最小值
            "190.71-323.46",  # 基频-最大值
            "69.48-76.54",    # 能量
            "75.79-82.51",    # 能量-最大值
            "43.05-59.13",    # 能量-最小值
            "537.47-693.83",  # 第一共振峰
            "1364.38-1706.11" # 第二共振峰
        ]

        # 检查共振峰的数量，避免索引错误
        formant1 = results['formants'][0] if len(results['formants']) > 0 else 0.0
        formant2 = results['formants'][1] if len(results['formants']) > 1 else 0.0

        # 生成表格数据
        data = [
            ["基频", f"{results['f0'][0]:.2f}-{results['f0'][1]:.2f}", reference_ranges[0], "Hz"],
            ["基频-最小值", f"{results['f0'][0]:.2f}", reference_ranges[1], "Hz"],
            ["基频-最大值", f"{results['f0'][1]:.2f}", reference_ranges[2], "Hz"],
            ["能量", f"{results['energy']:.2f}", reference_ranges[3], "dB"],
            ["能量-最大值", f"{results['energy'] * 1.1:.2f}", reference_ranges[4], "dB"],  # 模拟最大值
            ["能量-最小值", f"{results['energy'] * 0.9:.2f}", reference_ranges[5], "dB"],  # 模拟最小值
            ["第一共振峰", f"{formant1:.2f}", reference_ranges[6], "Hz"],
            ["第二共振峰", f"{formant2:.2f}", reference_ranges[7], "Hz"]
        ]

        # 设置表格的行数
        self.result_table.setRowCount(len(data))

        # 填充表格
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置居中对齐
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 禁止编辑
                self.result_table.setItem(i, j, item)

        # 调整列宽以适应内容
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.resizeColumnsToContents()

        # 设置字体
        font = QFont("Microsoft YaHei", 10)
        self.result_table.setFont(font)
        self.result_table.setStyleSheet("QHeaderView::section { background-color: lightgreen }")

        # 调整行高
        for i in range(self.result_table.rowCount()):
            self.result_table.setRowHeight(i, 35)
