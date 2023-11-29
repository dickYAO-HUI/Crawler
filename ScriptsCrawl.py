
import requests
from bs4 import BeautifulSoup
import os
import Util
from Crawl import BaseCrawler
class SfyCrawler(BaseCrawler):
    def parse(self):
        base_url="https://sfy.ru/scripts"
        response = requests.get(base_url, verify=False)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_links = soup.select("p a")
            links_array = [link['href'] for link in script_links]
        return links_array
    
    def crawl(self):
        os.makedirs(self.save_path + "/sfy", exist_ok=True)
        links = Util.add_domain_if_no_http(self.parse(), "https://sfy.ru")
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link):
        try:
            # 获取链接内容
            response = requests.get(link)
            response.raise_for_status()

            # 获取文件类型
            content_type = response.headers.get('Content-Type', '').lower()

            # 根据文件类型确定文件扩展名
            if 'text/html' in content_type:
                file_extension = 'html'
            elif 'application/pdf' in content_type:
                file_extension = 'pdf'
            else:
                file_extension = 'txt'

            # 从链接中提取文件名（以最后一个斜杠后的部分为文件名）
            file_name = link.rsplit('/', 1)[-1]
            file_name = Util.clean_filename(file_name)
            # 保存文件
            save_path = os.path.join(self.save_path+"\sfy", f"{file_name}.{file_extension}")
            with open(save_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"文件 {file_name} 下载完成，保存路径：{save_path}")
        except Exception as e:
            self.logger.error(f"下载文件时发生错误: {str(e)}")
class ScifiscriptsCrawler(BaseCrawler):
    def get_url(self,link):
        response = requests.get(link,headers=self.header)
        if response.status_code==200:
            # 使用BeautifulSoup解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            script_links = soup.find_all("a")
            # 剔除内部无关链接
            filtered_script_links = [link.get('href') for link in script_links if link.get('href').count('/') > 3]
            return filtered_script_links
        else:
            return []
    def parse(self):
        links=self.get_url("http://www.scifiscripts.com/scripts_a_m.html") + self.get_url("http://www.scifiscripts.com/scripts_n_z.html")
        return links
    def crawl(self):
        os.makedirs(self.save_path + "/sci", exist_ok=True)
        links=self.parse()
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link):
        try:
            # 获取链接内容
            response = requests.get(link)
            response.raise_for_status()

            # 获取文件类型
            content_type = response.headers.get('Content-Type', '').lower()

            # 根据文件类型确定文件扩展名
            if 'text/html' in content_type:
                file_extension = 'html'
            elif 'application/pdf' in content_type:
                file_extension = 'pdf'
            else:
                file_extension = 'txt'

            # 从链接中提取文件名（以最后一个斜杠后的部分为文件名）
            file_name = link.rsplit('/', 1)[-1]
            file_name = Util.clean_filename(file_name)
            # 保存文件
            save_path = os.path.join(self.save_path+"\Sci", f"{file_name}.{file_extension}")
            with open(save_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"文件 {file_name} 下载完成，保存路径：{save_path}")
        except Exception as e:
            self.logger.error(f"下载文件时发生错误: {str(e)}")
        pass
class AwesomefilmCrawler(BaseCrawler):
    def crawl(self):
        os.makedirs(self.save_path+"/Awesomefilm", exist_ok=True)
        links=self.parse()
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")
    def parse(self):
        url = "http://www.awesomefilm.com/"
        response = requests.get(url, verify=False)

        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            script_links = soup.find_all("a")
            links = [url+link.get('href') for link in script_links]
            return links
        return []

    def save_data(self,link):
        try:
            # 获取链接内容
            response = requests.get(link)
            response.raise_for_status()

            # 获取文件类型
            content_type = response.headers.get('Content-Type', '').lower()

            # 根据文件类型确定文件扩展名
            if 'text/html' in content_type:
                file_extension = 'html'
            elif 'application/pdf' in content_type:
                file_extension = 'pdf'
            else:
                file_extension = 'txt'

            # 从链接中提取文件名（以最后一个斜杠后的部分为文件名）
            file_name = link.rsplit('/', 1)[-1]
            file_name = Util.clean_filename(file_name)
            # 保存文件
            save_path = os.path.join(self.save_path+"\\Awesomefilm", f"{file_name}.{file_extension}")
            with open(save_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"文件 {file_name} 下载完成，保存路径：{save_path}")
        except Exception as e:
            self.logger.error(f"下载文件时发生错误: {str(e)}")
        pass
class moviescriptsandscreenplaysCrawler(BaseCrawler):
    def get_url(self,link):
        response = requests.get(link,headers=self.header)
        if response.status_code==200:
            # 使用BeautifulSoup解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('p b a')
            # 剔除内部无关链接
            links =[link.get("href") for link in links]
            return links
        else:
            return []
    def parse(self):
        links=self.get_url("https://moviescriptsandscreenplays.com/index.html")+self.get_url("https://moviescriptsandscreenplays.com/movie-scripts.html")+self.get_url("https://moviescriptsandscreenplays.com/movie-scripts2.html")
        return links
    def crawl(self):
        os.makedirs(self.save_path+"/moviescriptsandscreenplays", exist_ok=True)
        links=self.parse()
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link):
        try:
            # 获取链接内容
            response = requests.get(link)
            response.raise_for_status()

            # 获取文件类型
            content_type = response.headers.get('Content-Type', '').lower()

            # 根据文件类型确定文件扩展名
            if 'text/html' in content_type:
                file_extension = 'html'
            elif 'application/pdf' in content_type:
                file_extension = 'pdf'
            else:
                file_extension = 'txt'

            # 从链接中提取文件名（以最后一个斜杠后的部分为文件名）
            file_name = link.rsplit('/', 1)[-1]
            file_name = Util.clean_filename(file_name)
            # 保存文件
            save_path = os.path.join(self.save_path+"\moviescriptsandscreenplays", f"{file_name}.{file_extension}")
            with open(save_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"文件 {file_name} 下载完成，保存路径：{save_path}")
        except Exception as e:
            self.logger.error(f"下载文件时发生错误: {str(e)}")
        pass
        return super().save_data()