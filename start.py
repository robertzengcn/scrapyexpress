# -*- coding:UTF-8 -*-
from scrapy import Scrapy
import sys

print("Do you want to get data by search or by store?")
scrapytype = input("1.by search; 2.by store?\n")
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

def case2():
    print("2")    

def default():                       # 默认情况下执行的函数
    print('No such case') 

switch = {'1': case1,                # 注意此处不要加括号
          '2': case2,                # 注意此处不要加括号
          } 

switch.get(scrapytype, default)()