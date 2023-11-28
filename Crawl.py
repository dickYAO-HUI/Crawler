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
class XinanCrawler(BaseCrawler):
    def get_extract_last_page(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        last_page_element = soup.find('a', text='末页')
        last_page_url = last_page_element['href']
        last_page_value = int(last_page_url.split('=')[-1])
        return last_page_value
        
    def get_page_url(self,url,page):
        url=url+str(page)
        novel_response=requests.get(url,verify=False)
        if novel_response.status_code == 200:
            soup = BeautifulSoup(novel_response.text, 'html.parser')
            path_link=soup.find("div",class_="list_left_bot").select("div ul li a")
            links =["http://www.xnzjw.cn/"+a['href'] for a in path_link]
        else:
            return None
        return links
    def parse(self):
        all_url=[]
        page=1
        url="http://www.xnzjw.cn/list.aspx?i=72&page="
        response = requests.get(url,headers=self.header)
        if response.status_code==200:
            # 使用BeautifulSoup解析页面内容
            end_page=self.get_extract_last_page(response.text)
            while True :
                temp= self.get_page_url(url,page)
                if(page<=end_page):
                    all_url.extend(temp)
                    page=page+1
                else:
                    break
            return all_url
        else:
            return []
    def crawl(self):
        os.makedirs(self.save_path+"/Xinan", exist_ok=True)
        links=self.parse()
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.get_novel(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")
                
    def save_data(self,title, content):
        with open(self.save_path+"/Xinan/"+title+".txt", 'w', encoding='utf-8') as file:
            file.write(title + '\n\n')
            file.write(content)

    def get_novel(self,link):
        try:
            response = requests.get(link,headers=self.header)
            response.encoding = 'GBK'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取标题
            title_element = soup.find('h1')

        # Remove the <br> tags and their content
            for br in title_element.find_all('span'):
                br.extract()

            title = re.sub(r'\\|/\|\t', '', title_element.get_text(strip=True))
            print(title)

            # 提取内容
            content = soup.find('div', class_='list_left_bot').get_text()
            self.save_data(title,content)
        except Exception as e:
            print(f"发生异常：{e}"+link)

class TibetNovelCrawl(BaseCrawler):
    def get_page_NovelUrl(self,page):
        if page==1:
            url="https://www.tibetcul.com/wx/zuopin/xs/index.html"
        else:
            url="https://www.tibetcul.com/wx/zuopin/xs/index_"+str(page)+".html"
        novel_response=requests.get(url)
        if novel_response.status_code == 200: 
            soup = BeautifulSoup(novel_response.text, 'html.parser')
            path_link=soup.select("li div h6 a")
            links =["https://www.tibetcul.com"+a['href'] for a in path_link]
        else:
            return None
        return links
    def parse(self):
        page=1
        all_url=[]
        while True :
            temp= self.get_page_NovelUrl(page)
            if(temp!=None):
                all_url.extend(temp)
                page=page+1
            else:
                break
        for url in all_url:
            print(url)
        return all_url
    def crawl(self):
        os.makedirs(self.save_path+"/Tibet", exist_ok=True)
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
            response = requests.get(link,headers=self.header)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取标题
            title_element = soup.find('h2', class_='mb-4 font-weight-bold')
            title = title_element.text.strip() if title_element else "未找到标题"

            # 提取内容
            content_element = soup.find('div', class_='article-body')
            content = content_element.text.strip() if content_element else "未找到内容"
            with open(self.save_path+"./Tibet/"+title+".txt", 'w', encoding='utf-8') as file:
                file.write(title + '\n\n')
                file.write(content)
        except Exception as e:
            print(f"发生异常：{e}")
        return super().save_data()
    
class ChinawriterCrawler(BaseCrawler):
    def get_page_NovelUrl(self,page):
        if page==1:
            url="http://www.chinawriter.com.cn/404015/404017/index.html"
        else:
            url="http://www.chinawriter.com.cn/404015/404017/index"+str(page)+".html"
        novel_response=requests.get(url,verify=False)
        if novel_response.status_code == 200: 
            soup = BeautifulSoup(novel_response.text, 'html.parser')
            path_link=soup.find("div",class_="list_left").select("div ul li span a")
            links =[a['href'].replace('\n', '') for a in path_link]
            links=Util.add_domain_if_no_http(links,"http://www.chinawriter.com.cn/")
        else:
            return None
            
        return links

    def parse(self):
        page=1
        all_url=[]
        while True :
            temp= self.get_page_NovelUrl(page)
            if(temp!=None):
                all_url.extend(temp)
                page=page+1
            else:
                break
        return all_url
    def crawl(self):
        os.makedirs(self.save_path+"/Chinawriter", exist_ok=True)
        links=self.parse()
        for link in links:
            try:
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link)
                    self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link):
        if(link.__contains__("vip")):
            response = requests.get(link,headers=self.header)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取标题
            title_element = soup.find('div',class_="contBoxR").find('h1')

            title = re.sub(r'\\|/\|\t', '', title_element.get_text(strip=True))
            title=title.replace(u'|\xa0', '')
            # 提取内容
            content_element = soup.find('div', class_='contBoxR')
            content = content_element.get_text(separator='\n').strip() if content_element else "未找到内容"
            with open(self.save_path+"/Chinawriter/"+title+".txt", 'w', encoding='utf-8') as file:
                file.write(title + '\n\n')
                file.write(content)
        else:
            response = requests.get(link,headers=self.header)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取标题
            title_element = soup.find('em')
            title = re.sub(r'\\|/\|\t', '', title_element.get_text(strip=True))
            title=title.replace(u'|\xa0', '')
            title=Util.clean_filename(title)
            # 提取内容
            content = soup.find('div', class_='end_article').get_text()
            with open(self.save_path+"/Chinawriter/"+title+".txt", 'w', encoding='utf-8') as file:
                file.write(title + '\n\n')
                file.write(content)
        
if __name__ == "__main__":
    Chinawriter=ChinawriterCrawler(state_file="Chinawriter_statue.json",save_path="./Novel")
    Chinawriter.run()