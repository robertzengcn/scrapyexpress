import unittest
from scrapy import Scrapy
import time

class TestScrapy(unittest.TestCase):
    #python .\scrapy_test.py TestScrapy.testgetproductdetail
    def testgetproductdetail(self):
        sc=Scrapy()
        url="https://www.aliexpress.com/item/4000171398545.html?algo_pvid=6f2a8b66-d2a9-4e4a-aa6c-77d40724f61f&algo_expid=6f2a8b66-d2a9-4e4a-aa6c-77d40724f61f-10&btsid=0b86d80216066135805932798ec64f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
        sc.getproductdetail(url)
    #python .\scrapy_test.py TestScrapy.testgetitemfile
    def testgetitemfile(self):
        sc=Scrapy()
        sc.resultfile='G:\\scrapyexpress\\result\\'+str(time.time())+'.csv'
        file='G:\\scrapyexpress\\result\\2020-10-21\\mouse toy_test1.csv'
        sc.handleitembyfile(file,sc.resultfile)
        
if __name__ == '__main__':
    unittest.main()