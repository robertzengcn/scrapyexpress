from selenium import webdriver
class Scrapy(object):

    def __init__(self):
        self.browser = webdriver.Firefox()
    def startBykeyword(self,keyword):
        self.browser.get('https://www.aliexpress.com') 
        