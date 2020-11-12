from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from datetime import date
import csv 
import time
import re
from random import randint

class Scrapy(object):

    def __init__(self):
        
        self.browser = None
        self.pagenum=1

    def initbrowser(self,profiles=None):
        if profiles !=None:           
            fp = webdriver.FirefoxProfile(profiles)
            self.browser = webdriver.Firefox(fp)
        else:
            self.browser = webdriver.Firefox()
        
    def startBykeyword(self,keyword,profiles=None):
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        self.resultdirectory='./result/'+d1+'/'
        if not os.path.exists(self.resultdirectory):
            os.makedirs(self.resultdirectory)
        self.csvfile=self.resultdirectory+keyword+'_'+str(time.time())+'.csv'
        #profiles=r"C:\Users\robert zeng\AppData\Roaming\Mozilla\Firefox\Profiles\qcsnl19h.default-release"
        self.initbrowser()
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
        # allitemlist=[]
        # plist=self.getprolistinpage()
        
        # self.writedatacsv(plist)
        self.getlistpagew()
        nextpagdiv=self.browser.find_element_by_class_name('next-pagination-list')
        
        for i in range(2, self.pagenum):
            try:
                ibtn=nextpagdiv.find_element(By.XPATH, '//button[text()="'+str(i)+'"]')
                self.browser.execute_script("arguments[0].scrollIntoView();", ibtn)
                jscommand="var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"+ "var elementTop = arguments[0].getBoundingClientRect().top;"+ "window.scrollBy(0, elementTop-(viewPortHeight/2));"
                self.browser.execute_script(jscommand, ibtn)
                ibtn.click()
                self.browser.implicitly_wait(15)
                self.movetoitem("p4p")
                self.checkadexist()
                self.movetoitembyclass("next-pagination-list")

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
        self.movetoitem("p4p")
        
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
    def clickAdifram(self):
        raximglist=self.browser.find_elements_by_class_name('rax-image') 
        for raxi in raximglist:
            try:
                self.browser.implicitly_wait(2)
                raxi.click() 
            except TimeoutException:
                print("time out 202011051025171")
                return False
            except NoSuchElementException:
                print("not find 202011051025175")
                return False    

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
    #移动到feature product
    def movetoitem(self,item):
        self.scrolldownpage()
        p4p = self.browser.find_element_by_id(item)
        self.browser.execute_script("arguments[0].scrollIntoView();", p4p)
        actions = ActionChains(self.browser)
        actions.move_to_element(p4p).perform()
        jscommand="var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"+ "var elementTop = arguments[0].getBoundingClientRect().top;"+ "window.scrollBy(0, elementTop-(viewPortHeight/2));"
        self.browser.execute_script(jscommand, p4p)
    def movetoitembyclass(self,item):
        self.scrolldownpage()
        try:
            p4p = self.browser.find_element_by_class_name(item)
            self.browser.execute_script("arguments[0].scrollIntoView();", p4p)
            actions = ActionChains(self.browser)
            actions.move_to_element(p4p).perform() 
        except NoSuchElementException:
            print("not find 20201008124081")
            return False    
        # 把数据写入csv
    def writedatacsv(self,data):
        resdata=[]
        for word in data:
            resdata.append([word])

        file = open(self.csvfile, 'w+', newline ='')
        with file:     
            write = csv.writer(file) 
            write.writerows(resdata) 
    # 获取页面，写入csv
    def getlistpagew(self):
        plist=self.getprolistinpage()
        self.writedatacsv(plist)
    # 读取csv
    def readcsv(self,file):
        res=[]
        f = open(file, newline='')
        csv_reader = csv.reader(f)
        for row in csv_reader:
            res.append(row[0])
        return res 
        # 获取产品详情   
    def getproductdetail(self,pageurl):
        self.initbrowser()
        
        self.browser.get(pageurl)
        self.browser.maximize_window()
        # 慢慢滚动页面
        self.scrolldownpage()
        titlediv=self.browser.find_element_by_class_name('product-title')
        
        title=titlediv.text.strip()
        self.movetoitembyclass('product-title')
        pricestring=self.browser.find_element_by_class_name('product-price-value').text
        pricestring=pricestring.strip()
        lowprice=0
        heightprice=0
        substring = "-"
        try:
            pricestring.index(substring)
        except ValueError:
            # not find -
            lowprice=pricestring
            heightprice=pricestring
        else:
            plist=pricestring.split('-')
            lowprice=plist[0]
            dollpos=plist[0].find('$')
            if (dollpos!= -1):
                lowprice=plist[0][dollpos+1:].strip()
                heightprice=plist[1].strip()
        #获取产品主图
        mainimage=self.getMainimgurl()
        #处理sku
        productsku=self.browser.find_element_by_class_name('product-sku')
        oursku='AO'+str(int(time.time()))+str(randint(100, 999))
        skuwrap=productsku.find_elements_by_class_name('sku-property')
        #定义属性容器
        allattri={}
        self.closeiframead()
        for skudiv in skuwrap:
            # 检查文字属性
            skutitle=skudiv.find_element_by_class_name('sku-title').text
            # skutitle=skudiv.find_element_by_class_name('sku-title').text
            skukeypos=skutitle.find(':')
            if(skukeypos!=-1):
                skutitle=skutitle[0:skukeypos].strip()
            properitemlist=skudiv.find_elements_by_class_name('sku-property-item')
            allattri[skutitle]=[]
            # 检查是否是图片属性
            for pitem in properitemlist:
                try:                   
                    imgattr=pitem.find_element_by_tag_name('img') #查找图片属性                   
                    
                    imgattr.click()
                    self.browser.implicitly_wait(10)
                    mainimg=self.getMainimgurl()
                    
                    atttitle=imgattr.get_attribute("title")
                    attdic=dict(title=atttitle,image=mainimg)
                    allattri[skutitle].append(attdic)
                except TimeoutException:
                    print("time out 202010290929247")               
                except NoSuchElementException:
                    print("not find 202010290929249")    
                try:
                    protextdiv=pitem.find_element_by_class_name('sku-property-text')
                    prospantag=protextdiv.find_element_by_tag_name('span').text
                    attdic=dict(title=prospantag)
                    allattri[skutitle].append(attdic)
                except TimeoutException:
                    print("time out 202010291049266")               
                except NoSuchElementException:
                    print("not find 202010291049268")
        fulldata=dict(title=title,heightprice=heightprice,lowprice=lowprice,mainimg=mainimage,sku=oursku,allattribute=allattri)
        print(fulldata)
            
    # 获取产品页的主图               
    def getMainimgurl(self):
        try:
            mainimg=self.browser.find_element_by_class_name('magnifier-image')
            return mainimg.get_attribute("src")        
        except TimeoutException:
            print("time out 202010291047276")
            return None               
        except NoSuchElementException:
            print("not find 202010291047278") 
            return None 
    #关闭iframe中的广告
    def closeiframead(self):
        seq = self.browser.find_elements_by_tag_name('iframe')
        # print(len(seq))
        for index in range(len(seq)):
            try:
                self.browser.switch_to_default_content()
                iframe = self.browser.find_elements_by_tag_name('iframe')[index]
                name=iframe.get_attribute("name")
            
                self.browser.switch_to.frame(iframe)
                self.clickAdifram()
            except IndexError:
                print("iframe has been close 202011051030319")    
        self.browser.switch_to.default_content()    



    def handleitembyfile(self,file):
        if(not os.path.exists(file)):
            raise Exception('file not exist')
        listres=self.readcsv(file)#读取csv
        if not listres:
            raise Exception('file empty')
        # 循环遍历数组
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for i in listres:
            if re.match(regex, i) is not None:
              self.getproductdetail(i)
            else:
                continue


           







