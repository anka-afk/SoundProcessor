# 语音分析识别系统

## 环境设置

### 使用 Conda

1. 安装 [Anaconda](https://www.anaconda.com/products/distribution) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. 创建并激活环境:
   ```
   conda env create -f environment.yml
   conda activate 您的环境名称
   ```

### 使用 pip

如果您更喜欢使用 pip:

1. 创建虚拟环境:
   ```
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
   ```
2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

## 运行程序

安装完依赖后,运行以下命令启动程序:
```
python main.py
```

## 运行打包后的程序

1. 下载最新的发布版本。
2. 解压缩下载的文件。
3. 双击运行 `语音分析识别系统.exe`。

注意：首次运行可能需要一些时间来解压缩所有必要的文件。
