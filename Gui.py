import sys
from Crawl import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt

class SpiderThread(QThread):
    def __del__(self):
        self.spider.save_state()
    log_signal = pyqtSignal(str)

    def __init__(self, spider):
        super().__init__()
        self.spider = spider

    def run(self):
        try:
            self.spider.run()
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")
        finally:
            # 执行清理操作，确保关闭时保存状态
            self.spider.save_state()

class LogReaderThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file
        self.last_pos = 0

    def run(self):
        while True:
            with open(self.log_file, 'r') as f:
                f.seek(self.last_pos)
                new_logs = f.readlines()
                for log in new_logs:
                    self.log_signal.emit(log.strip())
                self.last_pos = f.tell()

            self.msleep(1000)

class MyGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.log_text = QTextEdit(self)
        self.start_button = QPushButton('Start Spider', self)
        self.start_button.clicked.connect(self.startSpider)

        vbox = QVBoxLayout()
        vbox.addWidget(self.log_text)
        vbox.addWidget(self.start_button)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Spider GUI')
        self.show()

    def startSpider(self):
        spider = SfyCrawler()  # 创建你的爬虫类实例
        self.spider_thread = SpiderThread(spider)
        self.spider_thread.log_signal.connect(self.updateLog)
        self.spider_thread.start()

        log_file = f"{spider.__class__.__name__}.log"
        self.log_reader_thread = LogReaderThread(log_file)
        self.log_reader_thread.log_signal.connect(self.updateLog)
        self.log_reader_thread.start()

    def updateLog(self, log):
        # 在文本框中显示实时日志
        self.log_text.append(log)

    def closeEvent(self, event):
        self.spider_thread.spider.save_state()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyGUI()
    sys.exit(app.exec_())
