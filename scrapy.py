from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
class Scrapy(object):

    def __init__(self):
        self.browser = webdriver.Firefox()
    def startBykeyword(self,keyword):
        self.browser.get('https://www.aliexpress.com')
        keyinput = self.browser.find_element_by_xpath('//*[@id="search-key"]')
        keyinput.send_keys(keyword)
        
        #serachbtn = self.browser.find_element_by_class_name('search-button')
        # self.closeadhome()#关闭首页可能出现的广告
        # serachbtn.click()
        keyinput.send_keys(Keys.ENTER)
        
        self.checkadexist()
        self.closeadultad()
        self.scrolldown()
        self.browser.implicitly_wait(2)#等待页面加载
        pagenum=self.getpagenum() #获取页面数量
        
        self.getprolistinpage()

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
            return False
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

        #totalpage=self.browser.find_element_by_class_name('total-page')
        totalpage = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'total-page'))
            )
        inner_text= self.browser.execute_script("return arguments[0].innerText;", totalpage)
        number=int(filter(inner_text.isdigit, inner_text))
        print(number)
        return number
    def getprolistinpage(self):
        #取产品列表外的div
        proclass=self.browser.find_element_by_class_name('product-list')  
        linkelems=proclass.find_elements_by_xpath("//a[@href]")
        for elem in linkelems:
            print(elem.get_attribute("href"))
    '''
    关闭首页的广告
    '''        
    def closeadhome(self):
        try:
            uinextad = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'rax-image'))
            )                  
        except TimeoutException:
            print("time out 20201008124076")
            return False
        except NoSuchElementException:
            print("not find 20201008124081")
            return False
        uinextad.click()
    '''
    滚动到页面底部
    '''    
    def scrolldown(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")    