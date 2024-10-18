from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt6.QtCore import Qt

class SummaryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []  # 初始化为空列表
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        title = QLabel("测试结果")
        title.setObjectName("summary-title")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        self.score_label = QLabel("总分: 0.00%")
        self.score_label.setObjectName("score-label")
        layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        restart_button = QPushButton("重新开始")
        restart_button.setObjectName("restart-button")
        restart_button.clicked.connect(self.parent().showWelcomeWindow)
        restart_button.setFixedWidth(200)
        
        layout.addStretch()
        layout.addWidget(restart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def update_results(self, results):
        self.results = results
        self.update_ui()

    def update_ui(self):
        # 清除之前的结果
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        for i, result in enumerate(self.results, 1):
            result_label = QLabel(f"第{i}题: {'正确' if result['correct'] else '错误'}")
            result_label.setObjectName("result-label")
            self.scroll_layout.addWidget(result_label)
            
            detail_label = QLabel(f"您的答案: {result['user_answer']}\n正确答案: {result['correct_answer']}")
            detail_label.setObjectName("detail-label")
            detail_label.setWordWrap(True)
            self.scroll_layout.addWidget(detail_label)
            
            self.scroll_layout.addWidget(QLabel(""))  # 添加空行作为分隔

        if self.results:
            score = sum(1 for r in self.results if r['correct']) / len(self.results) * 100
            self.score_label.setText(f"总分: {score:.2f}%")
        else:
            self.score_label.setText("总分: 0.00%")
