VERSION = "v1.6"

SaveAll_Flag = False        #全部保存爬虫记录
UrlDeDuplication = True     #URL去重
IfShowAll_Flag = False      #全部输出模式
ColorOutput = True          #彩色输出

LoadedUrl = []              #用于存储所有已请求过的URL，实现URL去重功能

RequestTimeout = 10         #单次请求超时设置
RequestHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "token=c4d038b4bed09fdb1471ef51ec3a32cd; v=114514md5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}                           #请求头


import requests
import csv
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup



#判断是否使用彩色输出
if ColorOutput == True:
    from colorama import init, Fore, Back, Style
    init()
else:
    class Fore:
        GREEN = WHITE = RED = ""
    class Style:
        RESET_ALL = ""



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
            #print(Fore.WHITE + "[ * ]  DEBUG: UrlLog-" + ToFullPath(url, hf))
            
    new_urls += links
    return new_urls

def web_crawl(urls, key, depth):
    #爬虫主函数
    print(Fore.WHITE + "[ * ]  DEBUG: Depth-" + str(depth))
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
            resp = requests.get(url, headers = RequestHeaders, timeout = RequestTimeout)
            resp.encoding = resp.apparent_encoding
            html_source = resp.text
            
            #如果网页内容匹配
            if key in html_source:
                SaveCSV(url, depth)
                print(Fore.GREEN + "[ + ]  FOUND: Depth-" + str(depth) + "  Url-" + url)
            elif IfShowAll_Flag == True:
                print(Fore.WHITE + "[ - ]  UNMATCH: Depth-" + str(depth) + "  Url-" + url)

            #如果开启记录所有爬取的URL模式
            if SaveAll_Flag == True:
                SaveAllCSV(url, depth)

            #如果开启URL去重模式
            if UrlDeDuplication == True:
                LoadedUrl.append(url)
            
            UrlList = getUrls(url, html_source)
            all_Url += UrlList
            
        except Exception as e:
            print(Fore.RED + "[ - ]  ERROR: Depth-" + str(depth) + "  Url-" + url)

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
    SearSpy Tool ''' + VERSION + '''
    ''')
    
    url = input('Please enter the target link: ')
    key = input('Please enter the keyword: ')
    depth = int(input('Please enter the maximum recursion depth: '))
    IfSaveAllUrl = input('Do you want to save all crawled links? [y/N] ')
    IfShowAll = input('Do you want to display all outputs? [y/N] ')
    
    if IfSaveAllUrl.lower() == "y":
        SaveAll_Flag = True
    else:
        SaveAll_Flag = False

    #是否开启调试模式
    if IfShowAll.lower() == "y":
        IfShowAll_Flag = True
    else:
        IfShowAll_Flag = False
    
    print("[ * ]  M S G: Loading...")

    # 开始执行爬虫
    url = [url]
    web_crawl(url, key, depth)

    print(Style.RESET_ALL)
    print("[ * ]  M S G: Done!")
