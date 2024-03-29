from bs4 import BeautifulSoup
import os
import shutil

def fix_file_extensions(folder_path):
    # 创建html文件夹
    html_folder = os.path.join(folder_path, 'html')
    if not os.path.exists(html_folder):
        os.makedirs(html_folder)

    # 遍历文件夹中的文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # 如果是文件
        if os.path.isfile(file_path):
            # 检查文件后缀名是否有重复
            if '.' in file_name:
                print(file_name)
                parts = file_name.split('.')
                base_name = '.'.join(parts[:1])  # 保留第一个点前的内容
                extension = '.'.join(parts[1:])  # 保留第二个点后的内容
                new_file_name = f"{base_name}.{extension}"
                i = 1
                while os.path.exists(os.path.join(folder_path, new_file_name)):
                    new_file_name = f"{base_name}_{i}.{extension}"
                    i += 1
                if new_file_name != file_name:
                    os.rename(file_path, os.path.join(folder_path, new_file_name))
                    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
            # 如果是HTML文件，则转换成TXT并移动到html文件夹
        if file_name.endswith('.html'):
            txt_file = os.path.join(folder_path, file_name[:-5] + '.txt')
            html_to_txt(file_path, txt_file)
            shutil.move(file_path, html_folder)

def html_to_txt(html_file, txt_file):
    # 尝试不同的编码格式打开文件
    for encoding in ['utf-8-sig', 'latin1', 'utf-16']:
        try:
            with open(html_file, 'r', encoding=encoding) as f:
                html_content = f.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("Unable to decode HTML file with any supported encoding.")

    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取文本内容
    text_content = soup.get_text()

    # 写入TXT文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text_content)



folder_path = '/Users/liuwei/Desktop/crawl/Scripts/sfy'  # 替换为你的文件夹路径
fix_file_extensions(folder_path)