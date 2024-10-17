import os
os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from welcome_window import WelcomeWindow
from info_form_window import InfoFormWindow
from question_window import QuestionWindow
from video_interaction_window import VideoInteractionWindow
from styles import set_global_style
from summary_window import SummaryWindow

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as file:
        return json.load(file)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_question = 0
        self.results = []
        self.questions = load_questions()
        self.initUI()

        # 设置主窗口背景色和按钮样式
        from globalStyles import get_global_style
        self.setStyleSheet(get_global_style())

    def initUI(self):
        self.setWindowTitle("语音分析识别系统")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.welcome_window = WelcomeWindow(self)
        self.info_form_window = InfoFormWindow(self)
        self.question_windows = [QuestionWindow(self, q, i) for i, q in enumerate(self.questions)]
        self.video_interaction_window = VideoInteractionWindow(self)
        self.summary_window = SummaryWindow(self)

        self.central_widget.addWidget(self.welcome_window)
        self.central_widget.addWidget(self.info_form_window)
        for window in self.question_windows:
            self.central_widget.addWidget(window)
        self.central_widget.addWidget(self.video_interaction_window)
        self.central_widget.addWidget(self.summary_window)

        self.central_widget.setCurrentWidget(self.welcome_window)

    def showInfoForm(self):
        self.central_widget.setCurrentWidget(self.info_form_window)

    def showQuestionWindow(self):
        self.current_question = 0
        if self.question_windows:
            self.central_widget.setCurrentWidget(self.question_windows[self.current_question])
        else:
            print("没有可用的问题窗口")

    def show_next_question(self):
        self.current_question += 1
        if self.current_question < len(self.question_windows):
            self.central_widget.setCurrentWidget(self.question_windows[self.current_question])
        else:
            self.show_video_interaction()

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

    def show_video_interaction(self):
        self.central_widget.setCurrentWidget(self.video_interaction_window)

    def show_summary_window(self):
        self.summary_window.update_results(self.results)
        self.central_widget.setCurrentWidget(self.summary_window)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_global_style(app)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
