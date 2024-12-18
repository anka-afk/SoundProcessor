from PyQt6.QtWidgets import QApplication, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

def set_global_style(app):
    """设置全局样式"""
    app.setStyleSheet("""
        /* 全局样式 */
        QWidget {
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            font-size: 15px;
            background-color: #f9f9f9;
            color: #2c3e50;
        }

        QLabel {
            color: #34495e;
            background-color: transparent;
        }

        /* 按钮样式 */
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #43A047);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 8px;
            margin: 6px;
        }

        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43A047, stop:1 #388E3C);
        }

        QPushButton:pressed {
            background-color: #388E3C;
        }

        /* 主要按钮 */
        #start-button, #submit-button, #record-button, #restart-button {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1E88E5);
            font-size: 18px;
            padding: 15px 32px;
            border-radius: 10px;
        }

        #start-button:hover, #submit-button:hover, #record-button:hover, #restart-button:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E88E5, stop:1 #1976D2);
        }

        /* 输入框 */
        QLineEdit, QTextEdit {
            padding: 10px;
            border: 1px solid #dcdcdc;
            border-radius: 6px;
            background-color: #ffffff;
        }

        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4CAF50;
        }

        /* 标题 */
        #welcome-title {
            font-size: 38px;
            color: #2c3e50;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* 容器样式 */
        #spectrum-frame {
            border: 1px solid #dcdcdc;
            border-radius: 8px;
            background-color: #ffffff;
            padding: 12px;
        }

        /* 滚动条样式 */
        QScrollArea {
            border: none;
            background-color: transparent;
        }

        QScrollBar:vertical {
            background: #ececec;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: #c0c0c0;
            border-radius: 6px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
    """)

def add_shadow_effect(widget):
    """为指定的 widget 添加阴影效果"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(3)
    shadow.setYOffset(3)
    shadow.setColor(QColor(0, 0, 0, 80))  # 阴影颜色，半透明黑色
    widget.setGraphicsEffect(shadow)
