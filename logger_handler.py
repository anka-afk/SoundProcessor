import logging
import sys
import traceback
from PyQt6.QtWidgets import QMessageBox

def setup_logger():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def exception_hook(exctype, value, tb):
    logger = logging.getLogger(__name__)
    logger.critical(f"Uncaught exception: {exctype.__name__}: {value}", exc_info=True)
    error_msg = f"Uncaught exception: {exctype.__name__}: {value}"
    QMessageBox.critical(None, "错误", f"发生未捕获的异常: {exctype.__name__}: {value}\n\n请查看日志文件以获取详细信息。")
    traceback.print_tb(tb)

sys.excepthook = exception_hook
