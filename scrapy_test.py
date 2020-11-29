import unittest
from scrapy import Scrapy
import time

class TestScrapy(unittest.TestCase):

    def testgetproductdetail(self):
        sc=Scrapy()
        url="https://www.aliexpress.com/item/4001310257213.html?spm=a2g0o.detail.1000013.2.20cd1dc9m6lYrz&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.169870.0&scm_id=1007.13339.169870.0&scm-url=1007.13339.169870.0&pvid=fc0acb05-ae58-4e60-a020-300bf2ee008c&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.169870.0,pvid:fc0acb05-ae58-4e60-a020-300bf2ee008c,tpp_buckets:668%230%23131923%230_668%23808%233772%23885_668%23888%233325%2313_668%232846%238109%23290_668%232717%237561%23398_668%231000022185%231000066059%230_668%233468%2315615%23663"
        sc.getproductdetail(url)
    #python .\scrapy_test.py TestScrapy.testgetitemfile
    def testgetitemfile(self):
        sc=Scrapy()
        sc.resultfile='G:\\scrapyexpress\\result\\'+str(time.time())+'.csv'
        file='G:\\scrapyexpress\\result\\2020-10-21\\mouse toy_test1.csv'
        sc.handleitembyfile(file,sc.resultfile)
        
if __name__ == '__main__':
    unittest.main()