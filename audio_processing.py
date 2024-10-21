'''
audio_processing.py
音频处理的支持库
'''

import librosa
import numpy as np
from scipy.signal import find_peaks

# 读取音频
def load_audio(filepath):
    y, sr = librosa.load(filepath, sr = None)
    return y, sr

# 计算能量
def compute_energy(y):
    energy = librosa.feature.rms(y = y)[0]
    return energy

# 计算平均能量
def compute_avg_energy(energy):
    return np.mean(energy)

# 提取F0(基频)
def extract_f0(y, sr, start_time, end_time):
    y_segment = y[int(start_time * sr): int(end_time * sr)]
    pitches, magnitudes = librosa.core.piptrack(y = y_segment, sr = sr)
    
    # 取最大能量处基频为F0
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0: # 忽略无效值
            pitch_values.append(pitch)
    
    if len(pitch_values) == 0:
        f0_mean = np.mean(pitch_values)
    else:
        f0_mean = 0 # 无有效值
    return f0_mean

# 使用共振峰(F1,F2)的近似值
def extract_formants(y, sr, start_time, end_time):
    y_segment = y[int(start_time * sr): int(end_time * sr)]
    
    # 短时傅里叶变换拿频谱
    D = np.abs(librosa.stft(y_segment))
    
    # 频率索引算共振峰近似F1,F2
    freqs = librosa.core.fft_frequencies(sr = sr)
    f1_idx, _ = find_peaks(D.mean(axis = 1), distance = 20)
    
    if len(f1_idx) >= 2:
        f1_mean = freqs[f1_idx[0]] # 第一个共振峰
        f2_mean = freqs[f1_idx[1]] # 第二个共振峰
    else:
        f1_mean, f2_mean = 0, 0 # 无共振峰
    return f1_mean, f2_mean

# 声调
def determine_tone(f0_a1, f0_a2, f0_a3):
    if abs(f0_a2 - f0_a1) <= f0_a1 * 0.3:
        return "一声"
    elif (f0_a2 - f0_a3) >= f0_a1 * 0.3:
        return "四声"
    else:
        return "二三声"