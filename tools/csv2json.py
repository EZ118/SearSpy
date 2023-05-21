#用于将CSV文件转为Json字符串，便于数据处理

import sys
import os
import csv
import json


def main(fname):
    if not os.path.exists(fname):
        print("ERROR: file doesn't exist")
        return

    jsonpath = fname.replace(".csv", ".json")
    print(jsonpath)
    # 读取CSV文件
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # 将数据转换为JSON格式
    with open(jsonpath, 'w') as jsonfile:
        json.dump(data, jsonfile)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "/?" or sys.argv[1] == "--h":
            print("USAGE:")
            print("  -h               Displays help content")
            print("  <path>           Trans the current file")
        else:
            main(sys.argv[1])
    except:
        print("This is a programe for turning csv format to json format.")
        filename = input("File Path: ")
        main(filename)
