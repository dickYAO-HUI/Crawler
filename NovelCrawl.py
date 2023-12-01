from Crawl import BaseCrawler
import requests
from bs4 import BeautifulSoup
import os
import Util
import re
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
            self.logger.info(f"读取{url}")
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
                    self.logger.info(f"下载完成{link}")
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
            self.logger.info(f"读取{url}")
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
                    self.logger.info(f"下载完成{link}")
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
            self.logger.info(f"读取{url}")
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
                    self.logger.info(f"下载完成{link}")
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