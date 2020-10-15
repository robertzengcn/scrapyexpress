from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
class Scrapy(object):

    def __init__(self):
        
        self.browser = None
        self.pagenum=1
        
    def startBykeyword(self,keyword,profiles=None):
        #profiles=r"C:\Users\robert zeng\AppData\Roaming\Mozilla\Firefox\Profiles\qcsnl19h.default-release"
        if profiles !=None:           
            fp = webdriver.FirefoxProfile(profiles)
            self.browser = webdriver.Firefox(fp)
        else:
            self.browser = webdriver.Firefox()
        self.browser.get('https://www.aliexpress.com')
        keyinput = self.browser.find_element_by_xpath('//*[@id="search-key"]')
        keyinput.send_keys(keyword)

        cookies = self.browser.get_cookies()
        print(cookies)

        #serachbtn = self.browser.find_element_by_class_name('search-button')
        # self.closeadhome()#关闭首页可能出现的广告
        # serachbtn.click()
        keyinput.send_keys(Keys.ENTER)
        
        self.checkadexist()
        self.closeadultad()
        self.browser.implicitly_wait(2)
        self.scrolldown()
        # self.browser.implicitly_wait(2)#等待页面加载
        # self.scrolldown()
        
        pagenum=self.getpagenum() #获取页面数量
        print(pagenum)
        if pagenum>self.pagenum:
            self.pagenum=pagenum
        allitemlist=[]
        plist=self.getprolistinpage()
        allitemlist=allitemlist+plist#合并数组
        nextpagdiv=self.browser.find_element_by_class_name('next-pagination-list')
        
        for i in range(2, self.pagenum):
            try:
                ibtn=nextpagdiv.find_element(By.XPATH, '//button[text()="'+str(i)+'"]')
                ibtn.click()
                self.browser.implicitly_wait(5)
            except NoSuchElementException:
                print("not find 20201015102155")
       
        # for i in range(1, self.pagenum):
        #     self.scrolldown()
        #     currbtn=self.browser.find_element_by_class_name('next-current')
        #     self.checkadexist()
            
        #     self.browser.implicitly_wait(2)#等待页面加载
        #     linklist=self.getprolistinpage()
        #     print(linklist)
        # self.getprolistinpage()


    #检查页面是否有广告存在，存在就关闭 
    def checkadexist(self): 
        try:
            uinextad = WebDriverWait(self.browser, 5).until(
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
        #先滚动到页面中间
        # self.scrollcenter()
        # self.browser.implicitly_wait(2)#等待页面加载
        # self.scrolldown()#再滚动到页面底部
        # self.scrollcenter()
        self.scrolldownpage()
        p4p = self.browser.find_element_by_id("p4p")
        self.browser.execute_script("arguments[0].scrollIntoView();", p4p)
        actions = ActionChains(self.browser)
        actions.move_to_element(p4p).perform()
        totalpage=self.browser.find_element_by_class_name('total-page')
        totalpage = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'total-page'))
            )
        
        # p4p = self.browser.find_element_by_id("")
        # self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        inner_text= self.browser.execute_script("return arguments[0].innerText;", totalpage)
        # number=int(filter(inner_text.isdigit, inner_text))
        numarr=[int(s) for s in inner_text.split() if s.isdigit()]  
        return numarr[0]
    def getprolistinpage(self):
        #取产品列表外的div
        proclass=self.browser.find_element_by_class_name('product-list')  
        linkelems=proclass.find_elements_by_xpath("//a[@href]")
        substring = "/item/"
        res=[]
        for elem in linkelems:
            fulllink=elem.get_attribute("href")
            if fulllink.find(substring) != -1:
               res.append(fulllink)
        return res        

    #关闭首页的广告     
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

    #滚动到页面底部   
    def scrolldown(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
    #滚动到页面中间
    def scrollcenter(self):
         self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2);") 
    def scrolldownpage(self):
        
        # winsize=self.browser.get_window_size()
        # print(winsize)
        # winheight=winsize.get('height')
        winheight = self.browser.execute_script("return document.body.scrollHeight")
        print(winheight)
        wlist=list(range(1,10))
        for i in wlist:
            tarhig=i*0.1*winheight #目标高度
            command="window.scrollTo(0, "+str(tarhig)+");"
            print(command)
            self.browser.execute_script(command)
            self.browser.implicitly_wait(3.5)#等待页面加载


       

           