'''
main_process.py
入口
'''

import os
import glob
import numpy as np
import pandas as pd
from audio_processing import load_audio, compute_energy, compute_avg_energy, extract_f0, extract_formants, determine_tone

def process_audio(filepath):
    y, sr = load_audio(filepath)
    
    # 执行步骤1
    energy = compute_energy(y)
    avg_energy = compute_avg_energy(energy)
    
    # 持续时间
    duration = len(y) / sr
    timestamps = np.arange(0, duration, 0.01) # 时间戳
    
    segments = []
    
    # 执行步骤2
    for i in range(1, len(energy)):
        if energy[i] > avg_energy * 1.08:
            start = timestamps[i]
            end = start + 0.05
            if 0.05 <= end - start <= 0.8:
                segments.append((start, end))
    
    results = []
    
    # 对每个片段处理
    for segment in segments:
        start, end = segment
        seg_duration = end - start
        
        # 执行步骤3
        start_30 = start + 0.3 * seg_duration
        end_80 = start + 0.8 * seg_duration
        
        # 后续计算
        f0_mean = extract_f0(y, sr, start_30, end_80)
        f1_mean, f2_mean = extract_formants(y, sr, start_30, end_80)
        
        start_20 = start_30 - 0.2 * seg_duration
        end_20 = end_80 + 0.2 * seg_duration
        d0_a2 = extract_f0(y, sr, start_20, start_30)
        f0_a3 = extract_f0(y, sr, end_80, end_20)
        
        tone = determine_tone(f0_mean, d0_a2, f0_a3)
        
        results.append([f0_mean, f1_mean, f2_mean, tone, avg_energy])
        
    return results

def process_all(directory):
    audio_files = glob.glob(os.path.join(directory, "*.wav")) + \
                  glob.glob(os.path.join(directory, "*.mp3"))
    for filepath in audio_files:
        print("处理文件:", filepath)
        results = process_audio(filepath)
        
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_file = os.path.join(directory, f"{base_name}_results.csv")
        
        df = pd.DataFrame(results, columns = ["F0均值", "F1均值", "F2均值", "声调", "平均能量"])
        df.to_csv(output_file, index = False)
        
        print("结果保存到:", output_file)

if __name__ == "__main__":
    directory = "./"
    process_all(directory)