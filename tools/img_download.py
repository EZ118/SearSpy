#用于将CSV文件转为Json字符串，便于数据处理

IfConfirmAll = False
RequestHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "token=c4d038b4bed09fdb1471ef51ec3a32cd; v=114514md5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}                           #请求头

import sys
import os
import csv

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def DelEvalString(s):
    #该函数用于去除课件名中的敏感字符
    #该函数用于避免恶意课件的非法命名
    #造成的影响具体表现为：电脑用户无法删除、移动、修改下载的文件。
    s = s.replace("\\", "_").replace("/", "_").replace(":", "_").replace("\"", "_").replace(" ", "_")
    s = s.replace("*", "_").replace("?", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    return s

def request_download(IMAGE_URL, fn):
    r = requests.get(IMAGE_URL)
    with open(fn, 'wb') as f:
        f.write(r.content)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def downallImg(url):
    print("[msg] Download from: " + url)
    global RequestHeaders
    resp = requests.get(url, headers = RequestHeaders)
    page = BeautifulSoup(resp.text,"html.parser")  
    imglist = page.find_all("img")

    for img in imglist:
        try:
            imgurl = img.get("src")
            if "http:" not in imgurl and "https:" not in imgurl:
                imgurl = urljoin(url, imgurl)
            else:
                imgurl = imgurl
            imgname = os.path.basename(imgurl)
            imgname = DelEvalString(imgname)
            print("[msg] Start download: " + imgname)
            request_download(imgurl, "./imgs/" + imgname)
            print("[ok] Finish download: " + imgname)
        except:
            print("[err] url: " + img.get("src"))
        

def confirm(url):
    global IfConfirmAll
    ipt = ""
    if IfConfirmAll == False:
        ipt = input("Do you want to download images from (" + str(url) + ") ? [(Y)es/(N)o/(A)ll]")
    else:
        ipt = "y"

    if ipt.lower() == "y" or ipt.lower() == "yes":
        return True
    elif ipt.lower() == "n" or ipt.lower() == "no":
        return False
    elif ipt.lower() == "a" or ipt.lower() == "all":
        IfConfirmAll = True
        return True

def main(fname):
    mkdir("./imgs/")
    
    if not os.path.exists(fname):
        print("ERROR: file doesn't exist")
        return

    # 读取CSV文件
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    for item in data:
        url = item[0]    #url链接位于表格第一列
        if confirm(url) == True:
            downallImg(url)
        else:
            continue

    


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "/?" or sys.argv[1] == "--h":
            print("USAGE:")
            print("  -h               Displays help content")
            print("  <path>           Use the current file")
        else:
            main(sys.argv[1])
    except:
        print("This program is used to download all images in CSV files that link to the website.")
        filename = input("File Path: ")
        main(filename)
