import unittest
from scrapy import Scrapy

class TestScrapy(unittest.TestCase):

    def testgetproductdetail(self):
        sc=Scrapy()
        url="https://www.aliexpress.com/item/4000879601737.html?algo_pvid=194ae2a0-fabf-49f6-8647-94faeeffc739&algo_expid=194ae2a0-fabf-49f6-8647-94faeeffc739-0&btsid=0b86d81616032505551423621eed35&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
        sc.getproductdetail(url)
        
if __name__ == '__main__':
    unittest.main()