# -*- coding:UTF-8 -*-
from scrapy import Scrapy
import sys
import os

print("Do you want to get data by search or by file?")
scrapytype = input("1.by search; 2.by file?\n")
Scrapy=Scrapy()


def case1():
    msg="tell me the keyword, you want to use\n"
    keyword = input(msg)
    while len(keyword)<1:
        keyword = input(msg)
    profilemsg="tell me where you save firefox cookies(option)\n"
    profile= input(profilemsg)
    if(len(profile)<1):
        profile=None
    print("already start, wait for a moment...")    
    Scrapy.startBykeyword(keyword,profile)
# 通过文件方式处理连接
def case2():
    msg="tell me the file path\n"
    keyword = input(msg)
    while len(keyword)<1 or not os.path.exists(keyword):
        print("key word empty or file not exist") 
        keyword = input(msg)
    profilemsg="tell me where you save firefox cookies(option)\n"
    profile= input(profilemsg)
    if(len(profile)<1):
        profile=None
    print("already start, wait for a moment...")       
    Scrapy.handleitembyfile(keyword)    


def default():                       # 默认情况下执行的函数
    print('No such case') 

switch = {'1': case1,                # 注意此处不要加括号
          '2': case2,                # 注意此处不要加括号
          } 

switch.get(scrapytype, default)()