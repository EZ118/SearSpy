# SearSpy
A web crawl script, search while crawling   
   
## Introduction
该项目利用爬虫的原理进行搜索匹配所给关键词的网站，旨在提供全网搜索的功能，发现网络角落。   
This project utilizes the principle of crawling to search and match websites with given keywords, aiming to provide a full network search function and discover network corners.   
原理是在所给页面中找到所有链接，并访问他们，匹配是否符合关键词并记录，接着重复以上过程，从访问得到的内容中再得到链接，并执行搜索。   
The principle is to find all the links on the given page, visit them, match whether they match the keywords, and record them. Then, repeat the above process to obtain the links from the accessed content, and perform a search.   
   
## Usage
1. SearSpy.py   
Type this command to make sure that you have already installed the needed library. If not, it would install them automaticly.   
```shell
pip install -r requirements.txt
```
   
Double click (or `python3 ./SearSpy.py`) to run it.   
Type the website's URL you want to search in.   
Type your keyword (a word or a phrase is suggested)   
Type the Recursion Depth (author suggested to fill the number between 10 and 20, larger number is okey but useless)   
Type `y` or `Y` if you want to save all crawled links   
Type `y` or `Y` to enable URL deduplication mode (TIP: It's faster, but it needs larger RAM)   
   
2. /tools/csv2json.py   
Drag your csv file on its icon and release, or use `python3 cv2json.py <path>`, or run it and input the file path.   
   
## To Do
1. csvTool to enrich the crawled data
2. make it faster (multi-thread)