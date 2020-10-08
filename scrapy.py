from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Scrapy(object):

    def __init__(self):
        self.browser = webdriver.Firefox()
    def startBykeyword(self,keyword):
        self.browser.get('https://www.aliexpress.com')
        keyinput = self.browser.find_element_by_xpath('//*[@id="search-key"]')
        keyinput.send_keys(keyword)
        serachbtn = self.browser.find_element_by_class_name('search-button')
        serachbtn.click()
        
        self.checkadexist()
        self.closeadultad()

        pagenum=self.getpagenum() #获取页面数量
        

    '''
    检查页面是否有广告存在，存在就关闭
    '''    
    def checkadexist(self): 
        try:
            uinextad = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ui-newuser-layer-dialog'))
            )
            self.browser.find_element_by_class_name('ui-newuser-layer-dialog')
            nextad=uinextad.find_element_by_class_name("next-dialog-close")
        except TimeoutException:
            print("time out 20201008124032")
        except NoSuchElementException:
            print("not find 20201008124024")
            return False
        nextad.click()
    '''
    关闭成人提示
    '''    
    def closeadultad(self):    
        try:
            iamold=self.browser.find_element_by_class_name('law-18-dialog-yes')
        except NoSuchElementException:
            print('20201008124044')
            return False
        iamold.click() 
    # 获取总的页数    
    def getpagenum(self):
        totalpage=self.browser.find_element_by_class_name('total-page')
        inner_text= self.browser.execute_script("return arguments[0].innerText;", totalpage)
        number=int(filter(inner_text.isdigit, inner_text))
        print(number)
        return number