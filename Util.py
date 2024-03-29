import re
from bs4 import BeautifulSoup
def add_domain_if_no_http(strings_array, domain):
    result_array = []

    for string in strings_array:
        # 检查字符串中是否包含 "http"
        if "http" not in string:
            # 如果没有包含 "http"，则在前方添加 domain
            modified_string = domain + string
            result_array.append(modified_string)
        else:
            # 如果包含 "http"，直接添加到结果数组
            result_array.append(string)

    return result_array

def clean_filename(filename):
    # 定义非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # 从文件名中去除非法字符
    cleaned_filename = ''.join(char for char in filename if char not in illegal_chars)

    # 去除末尾的空格和点
    cleaned_filename = cleaned_filename.rstrip(' ').rstrip('.')

    return cleaned_filename

def extract_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_tag = soup.find('a')
    if link_tag:
        return link_tag.get('href')
    else:
        return None
def extract_a_content(html):
    a_pattern = r'<a\s+[^>]*?>(.*?)</a>'
    match = re.search(a_pattern, html)
    if match:
        return match.group(1)
    else:
        return None
    
def extract_content_after_a_before_p(html):
    start_index = html.find('</a')
    if start_index != -1:
        start_index = html.find('>', start_index) + 1
        end_index = html.find('</p>', start_index)
        if end_index != -1:
            content = html[start_index:end_index]
            # 删除 "-" 和 "by"
            content = content.replace("-", "").replace("by", "")
            return content.strip()  # 去除首尾空白
    return None


def extract_content_after_b_before_br(html):
    # 使用Beautiful Soup解析HTML字符串
    soup = BeautifulSoup(html, 'html.parser')

    # 提取</b>标签后<br/>前的内容
    b_tag = soup.find('b')
    if b_tag:
        # 查找</b>标签后的下一个兄弟节点，并提取其内容
        content = b_tag.find_next_sibling(text=True).strip()
        # 去除连字符 "-"
        content_without_hyphen = content.replace('-', '').strip()
        # 去除 "by"
        content_without_by = content_without_hyphen.replace('by', '').strip()
        return content_without_by
    else:
        return 'unknown'

def extract_additional_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    index_by = text.find("-by")
    index_script = text.find("1935 shooting script")
    if index_by != -1:
        by_content = text[index_by + 3 : index_script].strip()
    else:
        by_content = None
    script_content = text[index_script:].strip()
    return by_content, script_content