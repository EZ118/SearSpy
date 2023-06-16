#!/usr/bin/python
# -*- coding: UTF-8 -*-

#global VERSION, SaveAll_Flag, UrlDeDuplication, IfShowAll_Flag, ColorOutput, LoadedUrl, RequestTimeout, RequestHeaders, FileOutputDir, CurrentHostOnly, CurrentHost
VERSION = "v1.9.1"

SaveAll_Flag = False        #全部保存爬虫记录
UrlDeDuplication = True     #URL去重
IfShowAll_Flag = False      #全部输出模式
ColorOutput = True          #彩色输出
CurrentHostOnly = False     #仅爬取当前域名的网页
CurrentHost = "."           #存储输入的链接的域名，用于（仅爬取当前域名的网页）
FileOutputDir = "./"        #文件输出目录

LoadedUrl = []              #用于存储所有已请求过的URL，实现URL去重功能

RequestTimeout = 7          #单次请求超时设置
RequestHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "PHPSESSID=uot6nkdfbq5iqn8vpmq8o2gdk1; acw_tc=2760824c16863916513117373e2ef467a663010ee8486517d903ae1bb5b63d; ASPSESSIONIDCCQAABAQ=HBMHMFCCOOOCLJJEMFFPCHMK; ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}                           #请求头




import requests
import csv
import re
import sys
import urllib.parse
from bs4 import BeautifulSoup



#判断是否使用彩色输出
if ColorOutput == True:
    from colorama import init, Fore, Back, Style
    init()
else:
    class Fore: GREEN = WHITE = RED = ""
    class Style: RESET_ALL = ""



def SaveCSV(url, current_url):
    #保存在CSV中
    with open(FileOutputDir + '/search_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url, current_url])

def SaveAllCSV(url, current_url):
    #保存在CSV中（所有链接）
    with open(FileOutputDir + '/crawler_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url, current_url])

def ToFullPath(base_url, relative_url):
    #相对转绝对
    return urllib.parse.urljoin(base_url, relative_url)

def GetDomain(url):
    #获取当前链接中的域名
    return urllib.parse.urlparse(url).netloc

def getUrls(url, html_source):
    #初始化
    urls = new_urls = links = []

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
        elif hf[0:11] != "javascript:" and hf[0:7] != "mailto:":
            #如果是相对链接，且不是javascript代码或email地址
            links.append(ToFullPath(url, hf))
            
    new_urls += links
    return new_urls

def web_crawl(urls, key, depth):
    #爬虫主函数
    global LoadedUrl, CurrentHost, CurrentHostOnly, RequestTimeout
    urlen = len(urls)
    all_Url = []

    #输出提示信息
    print(Fore.WHITE + "[ * ]  DEBUG: Depth-" + str(depth) + "  UrlList-" + str(urlen))

    #如果链接列表不再有项，或者超出最大深度限制，那么结束爬虫
    if depth == 0 or urlen == 0:
        return;

    for url in urls:
        #如果URL重复
        if url in LoadedUrl:
            continue
        elif CurrentHostOnly == True and CurrentHost not in url:
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

def getParameter(argv):
    def SetIt(fstr, argv, default):
        oppCnt = 0
        for st in argv:
            if fstr in st:
                st = st.replace(fstr, "")
                return st
                break
            else:
                oppCnt += 1
        return default

    
    global SaveAll_Flag, UrlDeDuplication, IfShowAll_Flag, ColorOutput, FileOutputDir, CurrentHost, CurrentHostOnly, RequestTimeout
    DefaultUrl = "https://www.python.org/"
    DefaultKey = "Python"
    DefaultDepth = "5"
    
    
    if len(argv) <= 1:
        return False
    if "-h" in argv or "--h" in argv:
        print('''    Usage:
        --url:<TARGET URL>        set the target url (e.g. --url:https://www.python.org/)
        --output:<PATH>           set the output dir path (e.g. --output:./results/)
        --key:<STRING>            set the keyword (e.g. --key:Python)
        --depth:<NUM>             set the depth (e.g. --depth:5)
        --timeout:<NUM>           set timeout for each request (e.g. --timeout:5) (Default:7s)
        -h                        get help for commands
        -l                        display all
        -nc                       without colored output
        -nud                      without url deduplication
        -s                        save all crawled links
        -hl                       only for the current host
        
    About:
        This project is open source and follows the GPL-3.0 protocol.
        The following is the code repository link for this project:
            https://github.com/EZ118/SearSpy
            https://gitee.com/EZ118/SearSpy''')
        return True
    if "-l" in argv:
        IfShowAll_Flag = True
    if "-nc" in argv:
        ColorOutput = False
    if "-nud" in argv:
        UrlDeDuplication = False
    if "-s" in argv:
        SaveAll_Flag = True
    if "-hl" in argv:
        CurrentHostOnly = True

    
    DefaultUrl = SetIt("--url:", argv, DefaultUrl)              #判断是否有--url参数
    FileOutputDir = SetIt("--output:", argv, FileOutputDir)     #判断是否有--output参数
    DefaultKey = SetIt("--key:", argv, DefaultKey)              #判断是否有--key参数
    DefaultDepth = int(SetIt("--depth:", argv, DefaultDepth))   #判断是否有--depth参数
    RequestTimeout = int(SetIt("--timeout:", argv, RequestTimeout)) #判断是否有--timeout参数

    #输出获取到的参数信息，便于定位问题或下一次爬虫
    print("[ * ]  M S G: --url:" + DefaultUrl + " --key:" + DefaultKey + " --depth:" + str(DefaultDepth) + " --output:" + FileOutputDir + " --timeout:" + str(RequestTimeout))

    #开始执行！
    CurrentHost = GetDomain(DefaultUrl)
    web_crawl([DefaultUrl], DefaultKey, DefaultDepth)

    #爬取完成，输出提示并结束
    print(Style.RESET_ALL)
    print("[ * ]  M S G: Done!")
    return True

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
    
    cli = getParameter(sys.argv)
    if cli == True: sys.exit()
    
    url = input('Please enter the target link: ')
    key = input('Please enter the keyword: ')
    depth = int(input('Please enter the maximum recursion depth: '))
    IfSaveAllUrl = input('Do you want to save all crawled links? [y/N] ')
    IfShowAll = input('Do you want to display all outputs? [y/N] ')

    #判断是否保存所有爬取链接
    if IfSaveAllUrl.lower() == "y": SaveAll_Flag = True
    else: SaveAll_Flag = False

    #判断是否开启调试模式
    if IfShowAll.lower() == "y": IfShowAll_Flag = True
    else: IfShowAll_Flag = False
    
    print("[ * ]  M S G: Loading...")
    
    # 开始执行爬虫
    CurrentHost = GetDomain(url)
    web_crawl([url], key, depth)

    #爬取完成，输出提示并结束
    print(Style.RESET_ALL)
    print("[ * ]  M S G: Done!")
    print("")
    input("Press ENTER to exit...")
