import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from welcome_window import WelcomeWindow
from info_form_window import InfoFormWindow
from question_page import QuestionPage
from styles import set_global_style
from summary_window import SummaryWindow

questions = [
    {
        'title': '第一题',
        'content': '请你准备好,读/a/一直持续到你的极限。',
        'media': ["assets/images/question1.png"],  # 列表中的字符串
        'hint': '这是一个简单的问候语。',
        'answer': '啊'
    },
    {
        'title': '第二题',
        'content': '请你准备好, 读芭比不博, 读三遍。',
        'media': "assets/images/question2.png",  # 直接是字符串
        'hint': '这是一个有着悠久历史的城市。',
        'answer': '芭比不博'
    },
    {
        'title': '第三题',
        'content': '请观看视频。',
        'media': ["assets/images/question2.png"],
        'hint': '这是一个有着悠久历史的城市。',
        'answer': '北京'
    },
    # 可以继续添加更多题目...
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_question = 0
        self.results = []
        self.initUI()

        # 设置主窗口背景色和按钮样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def initUI(self):
        self.setWindowTitle("语音分析识别系统")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.welcome_window = WelcomeWindow(self)
        self.info_form_window = InfoFormWindow(self)
        self.question_pages = [QuestionPage(self.central_widget, q, i) for i, q in enumerate(questions)]
        self.summary_window = SummaryWindow(self)

        self.central_widget.addWidget(self.welcome_window)
        self.central_widget.addWidget(self.info_form_window)
        for page in self.question_pages:
            self.central_widget.addWidget(page)
            page.answer_correct.connect(self.show_next_question)

        self.central_widget.addWidget(self.summary_window)

        self.central_widget.setCurrentWidget(self.welcome_window)

    def showInfoForm(self):
        self.central_widget.setCurrentWidget(self.info_form_window)

    def showQuestionPage(self):
        self.current_question = 0
        self.central_widget.setCurrentWidget(self.question_pages[self.current_question])

    def show_next_question(self):
        self.current_question += 1
        if self.current_question < len(self.question_pages):
            self.central_widget.setCurrentWidget(self.question_pages[self.current_question])
        else:
            # 所有题目都回答完毕，显示结算页面
            self.summary_window.update_results(self.results)
            self.central_widget.setCurrentWidget(self.summary_window)

    def record_result(self, question_number, is_correct, user_answer, correct_answer):
        self.results.append({
            'question_number': question_number,
            'correct': is_correct,
            'user_answer': user_answer,
            'correct_answer': correct_answer
        })

    def showWelcomeWindow(self):
        self.current_question = 0
        self.results = []
        self.central_widget.setCurrentWidget(self.welcome_window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_global_style(app)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
