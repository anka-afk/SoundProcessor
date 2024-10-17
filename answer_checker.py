import difflib
import pypinyin
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

class AnswerChecker:
    @staticmethod
    def check_answer(recognized_text, correct_answer, callback=None):
        is_correct = recognized_text.lower().strip() == correct_answer.lower().strip()
        if callback:
            callback()
        return is_correct
