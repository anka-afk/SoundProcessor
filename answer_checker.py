import difflib
import pypinyin
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

class AnswerChecker:
    @staticmethod
    def check_answer(recognized_text, correct_answer, callback=None):
        # 将识别文本和正确答案转换为小写并去除首尾空格
        recognized_text = recognized_text.lower().strip()
        correct_answer = correct_answer.lower().strip()

        # 将识别文本和正确答案转换为拼音
        recognized_pinyin = ''.join(pypinyin.lazy_pinyin(recognized_text))
        correct_pinyin = ''.join(pypinyin.lazy_pinyin(correct_answer))

        # 计算文本相似度
        text_similarity = difflib.SequenceMatcher(None, recognized_text, correct_answer).ratio()
        pinyin_similarity = difflib.SequenceMatcher(None, recognized_pinyin, correct_pinyin).ratio()

        # 检查正确答案是否包含在识别文本中
        contains_answer = correct_answer in recognized_text

        # 设置相似度阈值
        similarity_threshold = 0.5

        # 判断是否正确
        is_correct = (text_similarity >= similarity_threshold or 
                      pinyin_similarity >= similarity_threshold or 
                      contains_answer)

        if callback:
            callback()

        logger.debug(f"识别文本: {recognized_text}")
        logger.debug(f"正确答案: {correct_answer}")
        logger.debug(f"文本相似度: {text_similarity}")
        logger.debug(f"拼音相似度: {pinyin_similarity}")
        logger.debug(f"包含答案: {contains_answer}")
        logger.debug(f"是否正确: {is_correct}")

        return is_correct
