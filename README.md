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

---

# JSON 文件编写指南

本项目使用 JSON 文件来配置题目、媒体资源和用户交互逻辑。以下是 JSON 文件的结构和编写规则。

---

## 文件结构

JSON 文件是一个数组，每个元素代表一个页面（题目）。页面可包含标题、描述内容、媒体资源、交互逻辑和步骤控制。

### **基本字段说明**

| 字段名        | 类型         | 必填 | 描述                               |
| ------------- | ------------ | ---- | ---------------------------------- |
| `title`       | 字符串       | 是   | 页面标题，显示在界面顶部。         |
| `content`     | 字符串       | 是   | 页面描述内容，指导用户操作。       |
| `media`       | 对象         | 否   | 媒体资源，支持图片或音频。         |
| `interaction` | 字符串       | 否   | 交互类型，目前支持 `record`。      |
| `steps`       | 数组         | 否   | 多步骤操作，例如等待、播放音频等。 |
| `answer`      | 字符串或对象 | 否   | 正确答案，用于录音结果的对比验证。 |

---

## **媒体资源字段**

`media` 字段用于指定页面所需的媒体资源（图片或音频）。

| 媒体字段名 | 类型   | 必填 | 描述                                |
| ---------- | ------ | ---- | ----------------------------------- |
| `type`     | 字符串 | 是   | 媒体类型，可选 `image` 或 `audio`。 |
| `path`     | 字符串 | 是   | 媒体文件路径，相对路径。            |

**示例**：

```json
"media": {
    "type": "image",
    "path": "assets/images/page1.png"
}
```

---

## **步骤控制（steps）**

`steps` 字段是一个数组，用于控制页面上的多步骤操作，例如播放音频、等待时间、开始录音等。

### **步骤字段说明**

| 字段名     | 类型   | 必填 | 描述                                                            |
| ---------- | ------ | ---- | --------------------------------------------------------------- |
| `action`   | 字符串 | 是   | 操作类型，如 `wait`、`play_audio`、`record`。                   |
| `duration` | 数字   | 否   | 持续时间，单位为秒（适用于 `wait` 和 `record`）。               |
| `type`     | 字符串 | 否   | 录音类型，可选 `manual` 或 `auto`（仅在 `record` 操作中使用）。 |
| `path`     | 字符串 | 否   | 媒体路径（适用于 `play_audio`）。                               |

**步骤类型示例**：

1. **等待步骤（wait）**：

   ```json
   {
     "action": "wait",
     "duration": 2
   }
   ```

2. **播放音频步骤（play_audio）**：

   ```json
   {
     "action": "play_audio",
     "path": "assets/audio/sample.mp3"
   }
   ```

3. **自动录音步骤（record）**：

   ```json
   {
     "action": "record",
     "type": "auto",
     "duration": 5
   }
   ```

4. **手动录音步骤（record）**：
   ```json
   {
     "action": "record",
     "type": "manual"
   }
   ```

---

## **完整示例**

以下是一个包含多个页面的完整 JSON 文件示例：

```json
[
  {
    "title": "页面1",
    "content": "请尽可能长时间稳定地发/a/，以你舒服的音量和音高为准。",
    "media": {
      "type": "image",
      "path": "assets/images/page1.png"
    },
    "interaction": "record",
    "answer": "/a/"
  },
  {
    "title": "页面10",
    "content": "请复述：妈妈骂哥哥。",
    "media": {
      "type": "audio",
      "path": "assets/audio/mom_scolds_brother.mp3"
    },
    "steps": [
      {
        "action": "wait",
        "duration": 2
      },
      {
        "action": "play_audio",
        "path": "assets/audio/mom_scolds_brother.mp3"
      },
      {
        "action": "record",
        "type": "auto",
        "duration": 5
      }
    ],
    "answer": "妈妈骂哥哥"
  }
]
```

---

## 编写注意事项

1. **文件格式**：JSON 文件必须符合标准格式，确保所有字符串使用双引号，属性之间用逗号分隔。
2. **路径规范**：
   - 图片路径存放在 `assets/images/` 文件夹中。
   - 音频路径存放在 `assets/audio/` 文件夹中。
3. **录音类型**：
   - **手动录音** (`manual`)：用户手动按按钮开始和结束录音。
   - **自动录音** (`auto`)：倒数 3 秒后自动开始录音，录音时间可配置。
4. **验证**：`answer` 字段用于对比用户录音的结果，仅在必要时提供。

---

## 目录结构示例

```
项目根目录/
│
├── assets/
│   ├── images/
│   │   ├── page1.png
│   │   └── story_image.png
│   ├── audio/
│   │   ├── mom_scolds_brother.mp3
│   │   └── sister_recollection.mp3
│
├── questions.json
└── README.md
```

---

## 常见问题

1. **Q**：`steps` 和 `media` 可以同时存在吗？  
   **A**：可以，`media` 用于显示图片或音频，`steps` 控制操作步骤（如播放音频或录音）。

2. **Q**：如何设置录音时间？  
   **A**：在 `steps` 中配置 `duration` 字段，单位为秒。例如：

   ```json
   { "action": "record", "type": "auto", "duration": 5 }
   ```

3. **Q**：如果没有 `steps` 会发生什么？  
   **A**：如果没有 `steps`，程序将仅显示 `content` 和 `media` 的内容。

---

本指南帮助您快速理解 JSON 文件的结构和编写规则，如有疑问，请参考示例或联系开发团队。
