import sys
from Crawl import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
from ScriptsCrawl import *
from NovelCrawl import *

class SpiderThread(QThread):
    def __del__(self):
        for spider in self.spiders:
            spider.save_state()
    log_signal = pyqtSignal(str)

    def __init__(self, spiders):
        super().__init__()
        self.spiders = spiders
        
    def run(self):
        try:
            for spider in self.spiders:
                spider.run()
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")
        finally:
            # 执行清理操作，确保关闭时保存状态
            for spider in self.spiders:
                spider.save_state()

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
        self.checkboxes = []
        self.initUI()

    def initUI(self):
        self.start_button = QPushButton('开始爬取', self)
        self.start_button.clicked.connect(self.startSpider)
        self.log_text = QTextEdit(self)
        self.checkbox_layout = QVBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.start_button)
        vbox.addLayout(self.checkbox_layout)
        vbox.addWidget(self.log_text)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Spider GUI')
        self.show()
        # 在 __initUI 方法中的 self.checkbox_layout 后添加以下代码
        for spider_class in [SfyCrawler,ScifiscriptsCrawler,AwesomefilmCrawler,moviescriptsandscreenplaysCrawler,XinanCrawler,TibetNovelCrawl,ChinawriterCrawler]:  # 添加更多的爬虫类
            checkbox = QCheckBox(spider_class.__name__, self)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)

    def startSpider(self):
        selected_spiders = [spider_class for spider_class, checkbox in zip([SfyCrawler, ScifiscriptsCrawler, AwesomefilmCrawler, moviescriptsandscreenplaysCrawler, XinanCrawler, TibetNovelCrawl, ChinawriterCrawler], self.checkboxes) if checkbox.isChecked()]

        if not selected_spiders:
            self.log_text.append("No spider selected.\n")
            return

        spiders = [spider_class(state_file=f"{spider_class.__name__}_state.json") for spider_class in selected_spiders]

        self.spider_thread = SpiderThread(spiders)
        self.spider_thread.log_signal.connect(self.updateLog)
        self.spider_thread.start()

        log_files = [f"{spider_class.__name__}.log" for spider_class in selected_spiders]
        self.log_reader_thread = LogReaderThread(log_files[0])  # Assuming only one log file for simplicity
        self.log_reader_thread.log_signal.connect(self.updateLog)
        self.log_reader_thread.start()

    def updateLog(self, log):
        # 在文本框中显示实时日志
        self.log_text.append(log)

    def closeEvent(self, event):
        if hasattr(self, 'spider_thread'):
            for spider in self.spider_thread.spiders:
                spider.save_state()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyGUI()
    sys.exit(app.exec_())
