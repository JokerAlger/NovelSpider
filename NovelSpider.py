import os
import re
import requests

# 需要抓取的网站首页
url = 'https://www.ibiquges.com/'

# 发送 GET 请求，并获取响应对象
response = requests.get(url)

# 获取响应对象的 HTML 内容，并指定字符编码为 utf-8
html = response.content.decode()
response.encoding = 'utf-8'

# 使用正则表达式从 HTML 页面中获取所有的链接
links = re.findall(r'<a.+?href=[\'"](.*?)[\'"].*?>', html)
links = [link for link in links if link.startswith('http') or link.startswith('https')]
links = list(set(links))

# 输出抓取到的链接
print('抓取成功，总共抓取到 {} 个链接\n'.format(len(links)) + str(links))

# 将抓取到的链接保存到文件中
with open("links.txt", "w") as f:
    for link in links:
        f.write(link + "\n")

# 遍历抓取到的链接并获取小说的章节内容
for url in links:

    # 发送 GET 请求，获取响应对象
    response_1 = requests.get(url)

    # 获取响应对象的 HTML 内容，并指定字符编码为 utf-8
    html_1 = response.text
    response_1.encoding  = 'utf-8'

    # 使用正则表达式从 HTML 页面中获取小说章节的链接
    chapter_href_list = re.findall(r'<dd><a href=\'(.*)\' >', html_1)

    # 设置基础 URL，方便后面拼接链接
    base_url = 'https://www.ibiquges.com/'

    # 发送 GET 请求，获取响应对象
    response_1 = requests.get(url)
    response_1.encoding = 'utf-8'

    # 发送 GET 请求，获取响应对象
    response = requests.get(url)
    response.encoding = 'utf-8'

    # 获取小说的章节内容
    chapter = response_1.text

    # 使用正则表达式从页面中获取小说名称，并对名称中的非法字符进行处理
    title_regx = r'<h1>(.*?)</h1>'
    novel_name = re.findall(title_regx, response_1.text)[0]
    novel_name = re.sub(r'[\\/:*?<>|]+', '', novel_name)  # 去除非法字符
    novel_name += '.txt'  # 添加文件后缀名

    # 遍历小说章节并获取章节内容
    count = 0
    with open (novel_name, 'a+', encoding="utf-8") as f:
        for x in chapter_href_list:
            # 发送 GET 请求，获取响应对象
            response_2 = requests.get(base_url + x)
            response_2.encoding = 'utf-8'

            # 使用正则表达式从页面中获取章节的标题和内容
            title_regx = r'<h1>(.*?)</h1>'
            content_regx = '<br />&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />'
            title = re.findall(title_regx, response_2.text)
            content = re.findall(content_regx, response_2.text)

            # 将章节标题和内容写入保存文件中
            f.write('--------' + title[0] + '--------' + '\n')
            for e in content:
                f.write(e + '\n')

            # 显示下载进度
            count += 1
            if count > 5:
                break
            print('小说：《'+str(novel_name[:-4])+'》 第{}章 '.format(count) + str(title)+' 爬取成功!')