
import re
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
            script_links = soup.select("p")
            # links_array = [link['href'] for link in script_links]
        for link in script_links:
            print(link)
        return script_links
    
    def crawl(self):
        os.makedirs(self.save_path + "/sfy", exist_ok=True)
        # links = Util.add_domain_if_no_http(self.parse(), "https://sfy.ru")
        links=self.parse()
        for i in range(len(links) - 1, -1, -1):
            html = links[i]
            try:
                html=str(html)
                link=Util.extract_link(html)
                name=Util.extract_a_content(html)
                addition=Util.extract_content_after_a_before_p(html)

                if not link.startswith("http"):
                    link = "https://sfy.ru" + link
                print(str(link)+'\n'+str(name)+'\n'+str(addition))
                if link not in self.visited_urls:  # 检查链接是否已经访问过
                    self.save_data(link,name,addition)
                    # self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link,name,addition):
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
            file_name = name
            file_author = addition
            file_name=file_name+'|'+file_author
            # 保存文件
            save_path = os.path.join(self.save_path+"/sfy", f"{file_name}.{file_extension}")
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
            save_path = os.path.join(self.save_path+"/Sci", f"{file_name}.{file_extension}")
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
            save_path = os.path.join(self.save_path+"/Awesomefilm", f"{file_name}.{file_extension}")
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
            links = soup.select('p')
            # 剔除内部无关链接
            # links =[link.get("href") for link in links]
            return links
        else:
            return []
    def parse(self):
        links=self.get_url("https://moviescriptsandscreenplays.com/index.html")+self.get_url("https://moviescriptsandscreenplays.com/movie-scripts.html")+self.get_url("https://moviescriptsandscreenplays.com/movie-scripts2.html")
        # for link in links:
        #      print(str(link) +'\n')
        return links
    def crawl(self):
        os.makedirs(self.save_path+"/moviescriptsandscreenplays", exist_ok=True)
        links=self.parse()
        for html in links:
            try:
                html=str(html)
                link=Util.extract_link(html)
                name=Util.extract_a_content(html)
                addition=Util.extract_content_after_b_before_br(html)
                print(str(link)+'\n'+str(name)+'\n'+str(addition))
                if link is None or name is None or addition is None:
                    continue
                # if link not in self.visited_urls:  # 检查链接是否已经访问过
                self.save_data(link,name,addition)
                # self.visited_urls.add(link)
            except Exception as e:
                self.logger.error(f"An error occurred while processing link {link}: {str(e)}")

    def save_data(self,link,name,additon):
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
            file_name = name
            file_author = additon
            # 保存文件
            file_name=file_name+'|'+file_author
            save_path = os.path.join(self.save_path+"/moviescriptsandscreenplays", f"{file_name}.{file_extension}")
            with open(save_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"文件 {file_name} 下载完成，保存路径：{save_path}")
        except Exception as e:
            self.logger.error(f"下载文件时发生错误: {str(e)}")
        pass
        return super().save_data()
    
class jubenproCrawl(BaseCrawler):
    def get_url(self,link):
        links =[]
        response = requests.get(link,headers=self.header)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('li a')
            links =[link.get("href") for link in links]
            links=["https://www.juben.pro"+link for link in links ]
            print("完成"+link+":")
            print(links) 
            return links

        else:
            return []
    def parse(self):
    # 尝试从文件中读取链接
        try:
            with open("中文剧本链接.txt", 'r', encoding='utf-8') as file:
                links = [line.strip() for line in file.readlines()]
            print("文件存在")
        except FileNotFoundError:
            # 如果文件不存在，则爬取链接并保存到文件
            links = []
            for i in range(16):
                url = "https://www.juben.pro/famous/?page=" + str(i)
                links += self.get_url(url)

            # 添加网址前缀
            links = ["https://www.juben.pro" + link for link in links]

            # 将链接保存到txt文件中
            filename = "中文剧本链接.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                for link in links:
                    file.write(link + '\n')

        return links

    def crawl(self):
        os.makedirs(self.save_path+"/jubenPro", exist_ok=True)
        links=self.parse()
        for link in links:
            self.save_data(link)
        
        
        
    def get_page_data(self,link):
        head = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0'}
        cookies={'Cookie':'TopNum=5; UserIC=220%2E246%2E252%2E167%2D20231218113909; ThisDevice=%E7%94%B5%E8%84%91; Hm_lvt_913cc44822a3aadac25b159defada9f5=1702870753; updateVipnum=yes; vipnum=0; ASPSESSIONIDAWTDBBCQ=NFPMLHLDNMDLNBFNLHFJGOEK; ComTitle=; readAgreementID=1703; LastTime%2Dm132132%40qq%2Ecom=2023%2F12%2F18+14%3A37%3A27; NewEmail=; EyeProtection=; ifpartner=; IfMustReal=; adminname=; company=; ifvip=; IsAdmin=; UsereduType=; NoReadInfoNum=0; utype=%E5%85%B6%E4%BB%96; LimitPower=%E6%AD%A3%E5%B8%B8; UserID=246862; lastIP=117%2E36%2E50%2E198; NoLogin=; AgreementID=1703; NoLoginEndTime=; NickName=liuwei666; ifpass=0; LoginOK=juben%2Epro; username=liuwei666; loginnum=1; ifpass%5Femail=1; yname=%E7%8E%8B%E8%80%80%E8%BE%89; ErrLoginNum=; lastlogin=2023%2F11%2F22+11%3A44%3A51; UID=C20231122956081766; password=b7d2cea5fb9bc892; RememberMe=ok; IfUnionMember=False; usex=%E7%94%B7; usertype=%E5%AD%A6%E7%94%9F; VipEndDate=2023%2D11%2D21; face=%2Fimg%5Fuserface%2Fdefault%2Dboy%2Fboy5%2Epng; Total%5FBadRecord=0; BannerOrderID%5FLast=2; Total%5Fmess=0; Total%5Fsd=0; Total%5Freply=0; Total%5Freply%5Fjubao=0; Total%5Freply%5Ffankui=0; CurrentBannerNo=3; Total%5Fgb=0; ASPSESSIONIDAWRABCDR=BHKIHAGAFEDBBAMBJDCMFLFA; UserLinkURL=user%5Fdetail%5Fother%2Easp; TotalNum=42; iReadArtID=%2D20041%2D%2D14712%2D%2D14708%2D%2D14692%2D%2D37589%2D%2D52525%2D%2D50%2D%2D21633%2D%2D6108%2D%2D24%2D; UserTypeWord=%E5%85%B6%E4%BB%96; ASPSESSIONIDQEQCDDCS=OKAFDJABIADAIFAOPDNAFOCA; MySearchKeywords=%2F%E6%88%91%E4%B8%8D%E6%98%AF%E8%8D%AF%E7%A5%9E%2F%E8%82%96%E7%94%B3%E5%85%8B%E7%9A%84%E6%95%91%E8%B5%8E%2F%E9%98%BFQ%E6%AD%A3%E4%BC%A0%2F; ComeUrl=http%3A%2F%2Fwww%2Ejuben%2Epro%2Fart%5Fdetail%2Easp%3Fid%3D24; ReadADID=5; ViewPages=124; ASPSESSIONIDQGTDDCCS=FGGGPBLBMAEOFLMCNKLBBMOD; Hm_lpvt_913cc44822a3aadac25b159defada9f5=1703122975'}
        response = requests.get(link,headers=head,cookies=cookies)
        response.raise_for_status()
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到指定id的div标签
        script_div = soup.find('div', {'id': 'tab1_div_1'})
        for tag in script_div.find_all(['div', 'br', 'a']):  # 添加需要排除的标签
            tag.decompose()
        # 提取div标签内部的文本内容
        script_text = '\n'.join([paragraph.strip() for paragraph in script_div.stripped_strings]) if script_div else "未找到指定id的div标签"
        print("完成"+link)

        # 打印或使用提取的文本
        return script_text
    def get_name(self,link):
        head = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0'}
        cookies={'Cookie':'TopNum=5; UserIC=220%2E246%2E252%2E167%2D20231218113909; ThisDevice=%E7%94%B5%E8%84%91; Hm_lvt_913cc44822a3aadac25b159defada9f5=1702870753; updateVipnum=yes; vipnum=0; ASPSESSIONIDAWTDBBCQ=NFPMLHLDNMDLNBFNLHFJGOEK; ComTitle=; readAgreementID=1703; LastTime%2Dm132132%40qq%2Ecom=2023%2F12%2F18+14%3A37%3A27; NewEmail=; EyeProtection=; ifpartner=; IfMustReal=; adminname=; company=; ifvip=; IsAdmin=; UsereduType=; NoReadInfoNum=0; utype=%E5%85%B6%E4%BB%96; LimitPower=%E6%AD%A3%E5%B8%B8; UserID=246862; lastIP=117%2E36%2E50%2E198; NoLogin=; AgreementID=1703; NoLoginEndTime=; NickName=liuwei666; ifpass=0; LoginOK=juben%2Epro; username=liuwei666; loginnum=1; ifpass%5Femail=1; yname=%E7%8E%8B%E8%80%80%E8%BE%89; ErrLoginNum=; lastlogin=2023%2F11%2F22+11%3A44%3A51; UID=C20231122956081766; password=b7d2cea5fb9bc892; RememberMe=ok; IfUnionMember=False; usex=%E7%94%B7; usertype=%E5%AD%A6%E7%94%9F; VipEndDate=2023%2D11%2D21; face=%2Fimg%5Fuserface%2Fdefault%2Dboy%2Fboy5%2Epng; Total%5FBadRecord=0; BannerOrderID%5FLast=2; Total%5Fmess=0; Total%5Fsd=0; Total%5Freply=0; Total%5Freply%5Fjubao=0; Total%5Freply%5Ffankui=0; CurrentBannerNo=3; Total%5Fgb=0; ASPSESSIONIDAWRABCDR=BHKIHAGAFEDBBAMBJDCMFLFA; UserLinkURL=user%5Fdetail%5Fother%2Easp; TotalNum=42; iReadArtID=%2D20041%2D%2D14712%2D%2D14708%2D%2D14692%2D%2D37589%2D%2D52525%2D%2D50%2D%2D21633%2D%2D6108%2D%2D24%2D; UserTypeWord=%E5%85%B6%E4%BB%96; ASPSESSIONIDQEQCDDCS=OKAFDJABIADAIFAOPDNAFOCA; MySearchKeywords=%2F%E6%88%91%E4%B8%8D%E6%98%AF%E8%8D%AF%E7%A5%9E%2F%E8%82%96%E7%94%B3%E5%85%8B%E7%9A%84%E6%95%91%E8%B5%8E%2F%E9%98%BFQ%E6%AD%A3%E4%BC%A0%2F; ComeUrl=http%3A%2F%2Fwww%2Ejuben%2Epro%2Fart%5Fdetail%2Easp%3Fid%3D24; ReadADID=5; ViewPages=124; ASPSESSIONIDQGTDDCCS=FGGGPBLBMAEOFLMCNKLBBMOD; Hm_lpvt_913cc44822a3aadac25b159defada9f5=1703122975'}
        response = requests.get(link,headers=head,cookies=cookies)
        response.raise_for_status()
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.select_one('.title')
        script_title = title_element.get_text(strip=True)
        return script_title
    def pageNum(self,link):
        head = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0'}
        cookies={'Cookie':'TopNum=5; UserIC=220%2E246%2E252%2E167%2D20231218113909; ThisDevice=%E7%94%B5%E8%84%91; Hm_lvt_913cc44822a3aadac25b159defada9f5=1702870753; updateVipnum=yes; vipnum=0; ASPSESSIONIDAWTDBBCQ=NFPMLHLDNMDLNBFNLHFJGOEK; ComTitle=; readAgreementID=1703; LastTime%2Dm132132%40qq%2Ecom=2023%2F12%2F18+14%3A37%3A27; NewEmail=; EyeProtection=; ifpartner=; IfMustReal=; adminname=; company=; ifvip=; IsAdmin=; UsereduType=; NoReadInfoNum=0; utype=%E5%85%B6%E4%BB%96; LimitPower=%E6%AD%A3%E5%B8%B8; UserID=246862; lastIP=117%2E36%2E50%2E198; NoLogin=; AgreementID=1703; NoLoginEndTime=; NickName=liuwei666; ifpass=0; LoginOK=juben%2Epro; username=liuwei666; loginnum=1; ifpass%5Femail=1; yname=%E7%8E%8B%E8%80%80%E8%BE%89; ErrLoginNum=; lastlogin=2023%2F11%2F22+11%3A44%3A51; UID=C20231122956081766; password=b7d2cea5fb9bc892; RememberMe=ok; IfUnionMember=False; usex=%E7%94%B7; usertype=%E5%AD%A6%E7%94%9F; VipEndDate=2023%2D11%2D21; face=%2Fimg%5Fuserface%2Fdefault%2Dboy%2Fboy5%2Epng; Total%5FBadRecord=0; BannerOrderID%5FLast=2; Total%5Fmess=0; Total%5Fsd=0; Total%5Freply=0; Total%5Freply%5Fjubao=0; Total%5Freply%5Ffankui=0; CurrentBannerNo=3; Total%5Fgb=0; ASPSESSIONIDAWRABCDR=BHKIHAGAFEDBBAMBJDCMFLFA; UserLinkURL=user%5Fdetail%5Fother%2Easp; TotalNum=42; iReadArtID=%2D20041%2D%2D14712%2D%2D14708%2D%2D14692%2D%2D37589%2D%2D52525%2D%2D50%2D%2D21633%2D%2D6108%2D%2D24%2D; UserTypeWord=%E5%85%B6%E4%BB%96; ASPSESSIONIDQEQCDDCS=OKAFDJABIADAIFAOPDNAFOCA; MySearchKeywords=%2F%E6%88%91%E4%B8%8D%E6%98%AF%E8%8D%AF%E7%A5%9E%2F%E8%82%96%E7%94%B3%E5%85%8B%E7%9A%84%E6%95%91%E8%B5%8E%2F%E9%98%BFQ%E6%AD%A3%E4%BC%A0%2F; ComeUrl=http%3A%2F%2Fwww%2Ejuben%2Epro%2Fart%5Fdetail%2Easp%3Fid%3D24; ReadADID=5; ViewPages=124; ASPSESSIONIDQGTDDCCS=FGGGPBLBMAEOFLMCNKLBBMOD; Hm_lpvt_913cc44822a3aadac25b159defada9f5=1703122975'}
        response = requests.get(link,headers=head,cookies=cookies)
        response.raise_for_status()
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, 'html.parser')
        page_list_element = soup.find('div', {'class': 'text-page-list'})

        # 获取所有页码的链接
        page_links = page_list_element.find_all('a')

        # 提取最后一页的页码
        last_page = int(page_links[-1].text)
        return last_page
    def save_data(self, link):
        try:
            # 获取链接内容
            script = []
            name = self.get_name(link)
            print("开始爬取" + name)

            # 检查文件是否已存在，存在则跳过下载
            file_path = f"Scripts/jubenPro/{name}.txt"
            if os.path.exists(file_path):
                print(f"脚本已存在，跳过下载: {file_path}")
                return

            script.append("《" + name + "》\n")
            pagenum = self.pageNum(link)
            for i in range(pagenum):
                pagelink = link.replace(".html", "") + "-" + str(i + 1) + "-ccontent-hp.html"
                script.append(self.get_page_data(pagelink))

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('\n\n'.join(script))
            print(f"爬取完成，数据保存在 {name}.txt 中")
        except Exception as e:
            print(f"发生错误: {e}")

def process_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    processed_lines = []
    for line in lines:
        # 使用正则表达式判断是否包含汉字
        has_chinese = re.search(r'[\u4e00-\u9fa5]', line)

        if has_chinese:
            # 使用正则表达式保留引号中的文字
            quoted_text = re.findall(r'“([^”]*)”', line)
            quoted_text = re.sub(r'^\d+\s+--\s+--\s+\((\d+)\)', r'\1', quoted_text)


            # 如果有引号中的文字，添加处理过的行
            if quoted_text:
                processed_lines.append('“' + ''.join(quoted_text) + '”')
            else:
                # 删除所有英文，以及标点符号和数字前后两格都没有汉字的行
                cleaned_line = re.sub(r'[a-zA-Z.,!?;\'"“”‘’]', '', line)
                if re.search(r'(?<![^\W\d])[\W\d]+(?![^\W\d])', cleaned_line):
                    processed_lines.append(cleaned_line.strip())  # 去掉末尾的换行

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(processed_lines))

    
if __name__ == '__main__':
    test=SfyCrawler()
    test.crawl()
    # html='<p><a href="http://home.online.no/~bhundlan/scripts/True_Romance.pdf" target="_blank">True Romance</a> by Quentin Tarantino</p>'
    # print(Util.extract_link(html))
    # print(Util.extract_a_content(html))
    # print(Util.extract_content_after_a_before_p(html))
