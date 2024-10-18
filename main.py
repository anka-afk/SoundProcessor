import os
os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
os.environ['QT_QPA_PLATFORM'] = 'windows:fontengine=freetype'
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from welcome_window import WelcomeWindow
from info_form_window import InfoFormWindow
from question_window import QuestionWindow
from video_interaction_window import VideoInteractionWindow
from styles import set_global_style
from summary_window import SummaryWindow
from PyQt6.QtGui import QPixmap
from main_window import MainWindow  # 假设您的主窗口类在 main_window.py 中
from utils import resource_path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_questions():
    questions_path = resource_path('questions.json')
    with open(questions_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_global_pixmap():
    return QPixmap(resource_path("path/to/image.png"))

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



def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    print("QApplication created")
    set_global_style(app)
    print("Global style set")
    
    # 测试资源加载
    test_image_path = resource_path("assets/images/question1.png")
    test_video_path = resource_path("assets/videos/video1.mp4")
    
    print(f"Test image path: {test_image_path}")
    print(f"Test video path: {test_video_path}")
    print(f"Image exists: {os.path.exists(test_image_path)}")
    print(f"Video exists: {os.path.exists(test_video_path)}")
    
    main_window = MainWindow()
    print("MainWindow created")
    main_window.show()
    print("MainWindow shown")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
