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

