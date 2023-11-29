from abc import ABC, abstractmethod
import logging
import json
import requests
from bs4 import BeautifulSoup
import os
import Util
import re
class BaseCrawler(ABC):
    def __init__(self, state_file="crawler_state.json",  save_path="./Scripts"):
        self.state_file = self._get_full_path(state_file)
        self.visited_urls = set()
        self.save_path = self._get_full_path(save_path)  # 新的保存路径属性
        self.header = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0'}
    
        # 配置日志
        self.logger = self._configure_logger()

    # 新方法，用于获取完整路径
    def _get_full_path(self, file_name):
        return os.path.join(os.getcwd(), file_name)

    def _configure_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)

        # 创建文件处理器并设置日志级别
        file_handler = logging.FileHandler(f"{self.__class__.__name__}.log")
        file_handler.setLevel(logging.INFO)

        # 创建控制台处理器并设置日志级别
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 将处理器添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.visited_urls = set(state.get('visited_urls', []))
        except FileNotFoundError:
            self.logger.warning(f"State file not found: {self.state_file}")

    def save_state(self):
        state = {'visited_urls': list(self.visited_urls)}
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def parse(self, html):
        pass

    @abstractmethod
    def save_data(self):
        pass

    def run(self):
        try:
            self.logger.info("Starting crawler...")
            self.load_state()
            self.crawl()
            self.save_state()
            self.logger.info("Crawling completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
        finally:
            self.save_state()
