#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
These functional tests cannot cover the whole functionality of ScrapyExpress
"""
from scrapy import Scrapy
from config import get_config
import logging
import unittest

base_config = get_config()
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)

class ScraperemailMinimalFunctionalTestCase(unittest.TestCase):
    '''
    insure we can get the product infor page correct
    python -m pytest tests/functional_tests.py::ScraperemailMinimalFunctionalTestCase::test_scrapy_product_info
    '''
    def test_scrapy_product_info(self):
        pageurl=r"https://www.aliexpress.com/item/2251832785588933.html?algo_pvid=5bcd1521-e5be-4466-a0af-38b08a96ba60&algo_exp_id=5bcd1521-e5be-4466-a0af-38b08a96ba60-4&pdp_ext_f=%7B%22sku_id%22%3A%2266589171962%22%7D&pdp_npi=2%40dis%21USD%21129.0%21116.1%21%21%21%21%21%400bb47a1a16664912679755551ecfce%2166589171962%21sea&curPageLogUid=7rN5j3dOjMzH"
        scrapyModel=Scrapy()
        res=scrapyModel.getproductdetail(pageurl)
        key_to_lookup='title'
        logger.info(res)
        logger.info(res.has_key(key_to_lookup))
        self.assertTrue(res.has_key(key_to_lookup))
        
if __name__ == '__main__':
    unittest.main()        



        