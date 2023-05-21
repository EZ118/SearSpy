import requests
import csv
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

SaveAll_Flag = False           #全部保存爬虫记录
UrlDeDuplication = False    #URL去重
LoadedUrl = []

payload = ""
#请求头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "token=ee7e1e1e7dbe7; v=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

def SaveCSV(url, current_url):
    #保存在CSV中
    with open('results_only.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url, current_url])

def SaveAllCSV(url, current_url):
    #保存在CSV中（所有链接）
    with open('results_all.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url, current_url])

def ToFullPath(base_url, relative_url):
    #相对转绝对
    return urljoin(base_url, relative_url)

def getUrls(url, html_source):
    #初始化
    urls = []
    new_urls=[]
    links = []

    #提取所有完整网址
    pageUrls = re.findall("https://[^>\";\']*\d", html_source) + re.findall("http://[^>\";\']*\d", html_source)
    for pageUrl in pageUrls:
        if pageUrl not in new_urls:
            new_urls.append(pageUrl)

    #提取所有相对链接
    soup = BeautifulSoup(html_source, 'html.parser')
    for tag in soup.find_all(href=True):
        hf = tag['href']
        if "http" in hf or "https" in hf:
            if hf not in links and hf not in new_urls:
                links.append(hf)
        else:
            links.append(ToFullPath(url, hf))
            #print("[ * ]  DEBUG: UrlLog-" + ToFullPath(url, hf))
            
    new_urls += links
    return new_urls

def web_crawl(urls, key, depth):
    print("[ * ]  DEBUG: Depth-" + str(depth))
    all_Url = []
    if depth == 0:
        return;

    for url in urls:
        #如果URL重复
        if url in LoadedUrl:
            continue
        html_source = ""
        try:
            #请求URL
            resp = requests.get(url, headers=headers)
            resp.encoding = resp.apparent_encoding
            html_source = resp.text
            
            #如果网页内容匹配
            if key in html_source:
                SaveCSV(url, depth)
                print("[ + ]  FOUND: Depth-" + str(depth) + "  Url-" + url)

            #如果开启记录所有爬取的URL模式
            if SaveAll_Flag == True:
                SaveAllCSV(url, depth)

            #如果开启URL去重模式
            if UrlDeDuplication == True:
                LoadedUrl.append(url)
            
            UrlList = getUrls(url, html_source)
            all_Url += UrlList
            
        except Exception as e:
            print("[ - ]  ERROR: Depth-" + str(depth) + "  Url-" + url)

    web_crawl(all_Url, key, depth - 1)

if __name__ == '__main__':
    # 输入要搜索的 url、关键词、最大深度和选项
    print('''
      ____                  ____              
     / ___|  ___  __ _ _ __/ ___| _ __  _   _ 
     \___ \ / _ \/ _` | '__\___ \| '_ \| | | |
      ___) |  __/ (_| | |   ___) | |_) | |_| |
     |____/ \___|\__,_|_|  |____/| .__/ \__, |
                                 |_|    |___/ 
    SearSpy Tool
    ''')
    
    url = input('Please enter the target link: ')
    key = input('Please enter the keyword: ')
    depth = int(input('Please enter the maximum recursion depth: '))
    IfSaveAllUrl = input('Do you want to save all crawled links? [y/N]')
    IfDeDuplication = input('Do you want to enable URL deduplication mode? (Faster speed, but larger RAM required) [y/N]')
    
    if IfSaveAllUrl == "y" or IfSaveAllUrl == "Y":
        SaveAll_Flag = True
    else:
        SaveAll_Flag = False

    #是否开启URL去重
    if IfDeDuplication == "y" or IfDeDuplication == "Y":
        UrlDeDuplication = True
    else:
        UrlDeDuplication = False
    
    print("[ * ]  MSG: Loading...")

    # 开始执行爬虫
    url = [url]
    web_crawl(url, key, depth)
    print("[ * ]  Done!")
