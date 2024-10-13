from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QFormLayout
from PyQt6.QtCore import Qt

class InfoFormWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        title = QLabel("个人信息")
        title.setObjectName("form-title")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(50, 0, 50, 0)
        form_layout.setSpacing(20)
        
        self.name_input = QLineEdit()
        self.name_input.setObjectName("input-field")
        self.name_input.setPlaceholderText("请输入您的姓名")
        form_layout.addRow("姓名:", self.name_input)
        
        self.age_input = QLineEdit()
        self.age_input.setObjectName("input-field")
        self.age_input.setPlaceholderText("请输入您的年龄")
        form_layout.addRow("年龄:", self.age_input)
        
        self.note_input = QTextEdit()
        self.note_input.setObjectName("input-field")
        self.note_input.setPlaceholderText("请输入备注信息（可选）")
        form_layout.addRow("备注:", self.note_input)
        
        layout.addLayout(form_layout)
        
        submit_button = QPushButton("提交并开始测试")
        submit_button.setObjectName("submit-button")
        submit_button.clicked.connect(self.submitInfo)
        submit_button.setFixedWidth(200)
        
        layout.addStretch()
        layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def submitInfo(self):
        name = self.name_input.text()
        age = self.age_input.text()
        note = self.note_input.toPlainText()
        
        if not name or not age:
            QMessageBox.warning(self, "警告", "姓名和年龄不能为空！")
            return
        
        info = f"提交的信息：\n姓名: {name}\n年龄: {age}\n备注: {note}"
        QMessageBox.information(self, "提交成功", info)
        
        # 跳转到题目页面
        self.parent().parent().showQuestionPage()
