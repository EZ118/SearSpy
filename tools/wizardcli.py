#!/usr/bin/python
# -*- coding: UTF-8 -*-

lang = "en"
langlist = {
    "EnterUrl":{
        "zh":"请输入爬虫起始链接：",
        "en":"Please enter the target link: "
    },
    "EnterKeyword":{
        "zh":"请输入搜索关键词（建议为单个字或词）：",
        "en":"Please enter your keyword (a word or a phrase is suggested): "
    },
    "EnterDepth":{
        "zh":"请输入爬虫遍历最大深度：",
        "en":"Please enter the maximum recursion depth: "
    },
    "IfSaveAll":{
        "zh":"您想要保存爬过的所有链接吗？（包括匹配和未匹配项）[y/N] ",
        "en":"Do you want to save all crawled links? [y/N] "
    },
    "IfOutputAll":{
        "zh":"您想开启全部输出模式吗？（弄清进度卡住的原因）[y/N] ",
        "en":"Do you want to display all outputs? [y/N] "
    },
    "IfColorOutput":{
        "zh":"您想开启彩色输出模式吗？（便于分辨）[y/N] ",
        "en":"Do you want to enable color-output mode? [y/N] "
    },
    "EnterOutputPath":{
        "zh":"请输入文件保存地址（默认为程序所在目录）：",
        "en":"Please enter the file save directory (default to the directory where the program is located): "
    },
    "IfHostLimit":{
        "zh":"您想在爬虫时仅匹配当前域名吗？（仅爬取相同域名下的网页）[y/N] ",
        "en":"Do you want to only match the current domain name when crawling? [y/N] "
    },
    "WellDone":{
        "zh":"好的，我们已知晓您的需求，以下是根据您给出的回答生成的指令参数：（输入到命令行可使用）",
        "en":"Okay, we are aware of your requirements. Here are the command parameters generated based on the answer you provided: (Input to the command line for use)"
    },
    #"":{
    #    "zh":"",
    #    "en":""
    #},
}


if __name__ == '__main__':
    # 输入要搜索的 url、关键词、最大深度和选项
    print('''
 ____                  ____              
/ ___|  ___  __ _ _ __/ ___| _ __  _   _ 
\___ \ / _ \/ _` | '__\___ \| '_ \| | | |
 ___) |  __/ (_| | |   ___) | |_) | |_| |
|____/ \___|\__,_|_|  |____/| .__/ \__, |
                            |_|    |___/ 
SearSpy Tool Wizard (CLI)
Welcome to the SearSpy Wizard Program!
This program is applicable to SearSpy v1.8
''')
    lang = input("Please select language [(C)hinese/(E)nglish] ")
    if lang.lower() == "c" or lang.lower() == "chinese":
        print("您选择中文，下面的指引将会用中文显示")
        lang = "zh"
    elif lang.lower() == "e" or lang.lower() == "english":
        print("If you choose English, the following guidelines will be displayed in English")
        lang = "en"
    else:
        print("Option does not exist! ( 选项不存在 ) ")
    
    url = "--url:" + input(langlist["EnterUrl"][lang])
    key = "--key:" + input(langlist["EnterKeyword"][lang])
    depth = "--depth:" + str(input(langlist["EnterDepth"][lang]))
    IfSaveAllUrl = input(langlist["IfSaveAll"][lang])
    IfShowAll = input(langlist["IfOutputAll"][lang])
    IfColorOutput = input(langlist["IfColorOutput"][lang])
    OutputPath = "--output:" + input(langlist["EnterOutputPath"][lang])
    IfHostLimit = input(langlist["IfHostLimit"][lang])

    if IfSaveAllUrl.lower == "y" or IfSaveAllUrl.lower == "yes":
        IfSaveAllUrl = "-s"
    if IfShowAll.lower == "y" or IfShowAll.lower == "yes":
        IfShowAll = "-l"
    if IfColorOutput.lower == "y" or IfColorOutput.lower == "yes":
        IfShowAll = ""
    else:
        IfShowAll = "-nc"
    if IfHostLimit.lower == "y" or IfHostLimit.lower == "yes":
        IfHostLimit = "-hl"

    print(langlist["WellDone"][lang])
    command = url + " " + key + " " + depth + " " + OutputPath + " " + IfSaveAllUrl + " " + IfShowAll + " " + IfColorOutput + " " + IfHostLimit
    print("[C M D] SearSpy.py " + command)
    print("[SHELL] python3 SearSpy.py " + command)
    print("")
    input("Press any key to exit...")
