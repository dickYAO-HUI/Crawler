# 爬虫应用程序

该应用程序旨在使用多个爬虫从各种网站抓取数据。每个爬虫对应一个特定的网站，并实现为一个单独的类。该应用程序提供两种用法：通过图形用户界面（GUI）和脚本。

## 目录

- 入门
  - [先决条件](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#先决条件)
  - [安装](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#安装)
- QT界面用法
  - [启动应用程序](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#启动应用程序)
  - [选择爬虫](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#选择爬虫)
  - [开始抓取](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#开始抓取)
  - [查看日志](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#查看日志)
- [脚本用法](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#脚本用法)
- [添加新爬虫](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#添加新爬虫)
- [贡献](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#贡献)
- [许可证](https://chat.openai.com/c/9e8783fc-6162-43a8-920a-a083f66155f9#许可证)

## 入门

### 先决条件

在运行应用程序之前，请确保已安装以下内容：

- Python 3.x
- PyQt5
- `requirements.txt` 中指定的其他依赖项

### 安装

1. 将存储库克隆到本地计算机：

```
bashCopy code
git clone https://github.com/your-username/your-repository.git
```

1. 导航到项目目录：

```
bashCopy code
cd your-repository
```

1. 安装所需的依赖项：

```
bashCopy code
pip install -r requirements.txt
```

## QT界面用法

### 启动应用程序

运行以下命令以启动图形用户界面：

```
bashCopy code
python Gui.py
```

### 选择爬虫

在GUI中，您将看到一个可用爬虫的列表，每个爬虫由一个复选框表示。通过选中相应的复选框来选择要运行的爬虫。

### 开始抓取

单击“开始抓取”按钮以启动抓取过程。该应用程序将使用单独的线程从所选的网站开始抓取。

### 查看日志

应用程序将在GUI底部的文本区域中显示日志。您可以监视抓取的进度以及在抓取过程中可能发生的任何错误。

## 脚本用法

您还可以通过脚本运行爬虫。在脚本中，您可以使用相同的方法执行，你需要在if __name__ == "__main__":创建你需要的类，并执行类中run方法

### 查看日志

日志会保存在项目文件夹中

## 添加新爬虫

要添加新的爬虫，请在 `Crawl.py` 文件中创建一个新类，该类继承自 `BaseCrawler` 类。实现所需的方法（`crawl`，`parse`，`save_data`）。更新GUI以包括新的爬虫。

## 爬取到的资源的路径

项目目录/你定义的目录/网站名称/*

## 贡献

欢迎贡献！如果您有任何想法、建议或改进，请提出问题或创建拉取请求。

## 许可证

该项目根据 MIT 许可证许可 - 有关详细信息，请参阅 [LICENSE](https://chat.openai.com/c/LICENSE) 文件。