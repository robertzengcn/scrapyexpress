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
from furl import furl
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import ElementClickInterceptedException
import logging
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)
class Scrapy(object):

    def __init__(self):

        self.browser = None
        self.pagenum = 1

    def initbrowser(self, profiles=None,binary=None):
        options = Options()
        options.binary_location = binary
        if profiles != None:
            fp = webdriver.FirefoxProfile(profiles)
            self.browser = webdriver.Firefox(fp,options=options)
        else:
            self.browser = webdriver.Firefox(options=options)

    def startBykeyword(self, keyword,profiles=None,binary=None):
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        self.resultdirectory = './result/'+d1+'/'
        if not os.path.exists(self.resultdirectory):
            os.makedirs(self.resultdirectory)
        self.csvfile = self.resultdirectory + \
            keyword+'_list'+str(time.time())+'.csv'
        self.resultfile = self.resultdirectory + \
            keyword+'_result'+str(time.time())+'.csv'
        #profiles=r"C:\Users\robert zeng\AppData\Roaming\Mozilla\Firefox\Profiles\qcsnl19h.default-release"
        self.initbrowser(profiles,binary)
        self.browser.get('https://www.aliexpress.com')
        keyinput = self.browser.find_element_by_xpath('//*[@id="search-key"]')
        keyinput.send_keys(keyword)

        # cookies = self.browser.get_cookies()
        # print(cookies)

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
        self.closeiframead()
        pagenum = self.getpagenum()  # 获取页面数量
        print(pagenum)
        if pagenum > self.pagenum:
            self.pagenum = pagenum
        # allitemlist=[]
        # plist=self.getprolistinpage()

        # self.writedatacsv(plist)
        self.getlistpagew()
        try:
            self.scrapyListpage(self.pagenum)
        except StaleElementReferenceException:
            # print("get list error, may be alread at end of list page 20201128174577")
            logger.info("get list error, may be alread at end of list page 20201128174577") 
        # 读取列表结果csv
        self.handleitembyfile(self.csvfile,self.resultfile)
        # print("complete\n")
        # print("list file locate:\n")
        # print(self.csvfile+"\n")
        logger.info(self.csvfile)
        # print("result file locate:\n")
        # print(self.resultfile+"\n")
        logger.info(self.resultfile)
        # for i in range(1, self.pagenum):
        #     self.scrolldown()
        #     currbtn=self.browser.find_element_by_class_name('next-current')
        #     self.checkadexist()

        #     self.browser.implicitly_wait(2)#等待页面加载
        #     linklist=self.getprolistinpage()
        #     print(linklist)
        # self.getprolistinpage()
    # 抓取列表页
    def scrapyListpage(self, pagenum):
        nextpagdiv = self.browser.find_element_by_class_name(
            'next-pagination-list')

        for i in range(2, pagenum):
            try:
                ibtn = nextpagdiv.find_element(
                    By.XPATH, '//button[text()="'+str(i)+'"]')
                self.browser.execute_script(
                    "arguments[0].scrollIntoView();", ibtn)
                jscommand = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" + \
                    "var elementTop = arguments[0].getBoundingClientRect().top;" + \
                    "window.scrollBy(0, elementTop-(viewPortHeight/2));"
                self.browser.execute_script(jscommand, ibtn)
                ibtn.click()
                self.browser.implicitly_wait(15)
                try:
                    self.movetoitem("p4p")
                except NoSuchElementException:  
                    print("p4p not find 202011281757114")
                    self.scrolldownpage() 
                    self.movetoitembyclass("list-pagination")
                self.checkadexist()
                self.movetoitembyclass("next-pagination-list")
                self.getlistpagew()
                # self.movetoitembyclass("next-pagination-list")
                # self.browser.implicitly_wait(2)
            except NoSuchElementException:
                print("not find 20201015102155")

    # 检查页面是否有广告存在，存在就关闭
    def checkadexist(self):
        try:
            uinextad = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'ui-newuser-layer-dialog'))
            )
            self.browser.find_element_by_class_name('ui-newuser-layer-dialog')
            nextad = uinextad.find_element_by_class_name("next-dialog-close")
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
            iamold = self.browser.find_element_by_class_name(
                'law-18-dialog-yes')
        except NoSuchElementException:
            print('20201008124044')
            return False
        try:    
            iamold.click()
        except ElementClickInterceptedException:
            self.browser.execute_script("arguments[0].click();", iamold)
    # 获取总的页数

    def getpagenum(self):
        # 先滚动到页面中间
        # self.scrollcenter()
        # self.browser.implicitly_wait(2)#等待页面加载
        # self.scrolldown()#再滚动到页面底部
        # self.scrollcenter()
        try:
            self.movetoitem("p4p")
        except NoSuchElementException:
            self.scrolldownpage()
            self.movetoitembyclass("list-pagination") 
        totalpage = self.browser.find_element_by_class_name('total-page')
        totalpage = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'total-page'))
        )

        # p4p = self.browser.find_element_by_id("")
        # self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        inner_text = self.browser.execute_script(
            "return arguments[0].innerText;", totalpage)
        # number=int(filter(inner_text.isdigit, inner_text))
        numarr = [int(s) for s in inner_text.split() if s.isdigit()]
        return numarr[0]

    def getprolistinpage(self):
        # 取产品列表外的div
        proclass = self.browser.find_element_by_class_name('JIIxO')
        linkelems = proclass.find_elements_by_xpath("//a[@href]")
        substring = "/item/"
        res = []
        for elem in linkelems:
            fulllink = elem.get_attribute("href")
            if fulllink.find(substring) != -1:
                res.append(fulllink)
        return res

    # 关闭首页的广告
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
        raximglist = self.browser.find_elements_by_class_name('rax-image')
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

    # 滚动到页面底部
    def scrolldown(self):
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    # 滚动到页面中间
    def scrollcenter(self):
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight/2);")

    def scrolldownpage(self):

        # winsize=self.browser.get_window_size()
        # print(winsize)
        # winheight=winsize.get('height')
        winheight = self.browser.execute_script(
            "return document.body.scrollHeight")
        print(winheight)
        wlist = list(range(1, 10))
        for i in wlist:
            tarhig = i*0.1*winheight  # 目标高度
            command = "window.scrollTo(0, "+str(tarhig)+");"
            print(command)
            self.browser.execute_script(command)
            self.browser.implicitly_wait(3.5)  # 等待页面加载

    # 移动到feature product
    def movetoitem(self, item):
        self.scrolldownpage()
        p4p = self.browser.find_element_by_id(item)
        self.browser.execute_script("arguments[0].scrollIntoView();", p4p)
        actions = ActionChains(self.browser)
        actions.move_to_element(p4p).perform()
        jscommand = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" + \
            "var elementTop = arguments[0].getBoundingClientRect().top;" + \
            "window.scrollBy(0, elementTop-(viewPortHeight/2));"
        self.browser.execute_script(jscommand, p4p)

    def movetoitembyclass(self, item):
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
    def writedatacsv(self, data):
        resdata = []
        for word in data:
            resdata.append([word])

        file = open(self.csvfile, 'w+', newline='')
        with file:
            write = csv.writer(file)
            write.writerows(resdata)

    # 获取页面，写入csv
    def getlistpagew(self):
        self.closeiframead()
        plist = self.getprolistinpage()
        self.writedatacsv(plist)

    # 读取csv
    def readcsv(self, file):
        res = []
        with open(file, newline='') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                res.append(row[0])
            return res

        # 取产品简介
    def getspecial(self):
        try:
            itemtabs= self.browser.find_elements_by_xpath('//*[text()="SPECIFICATIONS"]')
            itemtab=itemtabs[1]
            self.browser.execute_script("arguments[0].scrollIntoView();", itemtab)
            # actions = ActionChains(self.browser)
            # actions.move_to_element(itemtab).perform()
            self.closeiframead()
            try:
                for i in itemtabs:
                    i.click()
            except ElementClickInterceptedException:
                print("tab not clickable")
            # actions.perform()
            self.browser.implicitly_wait(2)
            productspec = self.browser.find_element_by_class_name(
            'product-specs').text
            return productspec
        except NoSuchElementException:
            print("not find product special text")
            return None
    # 移除HTML,除了img, br        
    def cleanhtml(self,raw_html):
        cleanr = re.compile(r'<(?!img).*?>')
        cleantext = cleanr.sub('', raw_html)
        return cleantext

        # 获取产品详情
    def getproductdetail(self, pageurl):
        if self.browser==None:
            self.initbrowser()

        self.browser.get(pageurl)
        self.browser.maximize_window()
        # 慢慢滚动页面
        self.scrolldownpage()
        titlediv = self.browser.find_element_by_class_name('product-title')

        title = titlediv.text.strip()
        self.movetoitembyclass('product-title')
        try:
            pricestring = self.browser.find_element_by_class_name(
            'product-price-value').text
        except NoSuchElementException:
            pricestring = self.browser.find_element_by_class_name(
            'uniform-banner-box-price').text
        pricestring = pricestring.strip()
        lowprice = 0
        heightprice = 0
        substring = "-"
        try:
            pricestring.index(substring)
        except ValueError:
            # not find -
            lowprice = pricestring
            heightprice = pricestring
        else:
            plist = pricestring.split('-')
            lowprice = plist[0]
            dollpos = plist[0].find('$')
            if (dollpos != -1):
                lowprice = plist[0][dollpos+1:].strip()
                heightprice = plist[1].strip()
        # 获取产品主图
        mainimage = self.getMainimgurl()
        # 处理sku
        productsku = self.browser.find_element_by_class_name('product-sku')
        oursku = 'AO'+str(int(time.time()))+str(randint(100, 999))
        skuwrap = productsku.find_elements_by_class_name('sku-property')
        # 处理url
        purl = furl(pageurl).remove(args=True, fragment=True).url
       
       
        specialtxt = self.getspecial()

        # 定义属性容器
        allattri = {}
        self.closeiframead()
        # 定义其他图片属性
        otherimglist = self.getOimages()
        # 处理详情
        itemdetaildiv=self.browser.find_element_by_id('product-description')
        detailhtml=itemdetaildiv.get_attribute('innerHTML')
        detailhtml=self.cleanhtml(detailhtml)
        for skudiv in skuwrap:
            # 检查文字属性
            skutitle = skudiv.find_element_by_class_name('sku-title').text
            # skutitle=skudiv.find_element_by_class_name('sku-title').text
            skukeypos = skutitle.find(':')
            if(skukeypos != -1):
                skutitle = skutitle[0:skukeypos].strip()
            properitemlist = skudiv.find_elements_by_class_name(
                'sku-property-item')
            allattri[skutitle] = []
            # 检查是否是图片属性
            for pitem in properitemlist:
                try:
                    imgattr = pitem.find_element_by_tag_name('img')  # 查找图片属性
                         
                    imgattr.click()
                    self.browser.implicitly_wait(10)
                    mainimg = self.getMainimgurl()

                    atttitle = imgattr.get_attribute("title")
                    attdic = dict(title=atttitle, image=mainimg)
                    allattri[skutitle].append(attdic)
                except TimeoutException:
                    print("time out 202010290929247")
                except NoSuchElementException:
                    print("not find 202010290929249")
                except ElementClickInterceptedException:
                    print("attribute not availbale 202011291135393")    
                try:
                    protextdiv = pitem.find_element_by_class_name(
                        'sku-property-text')
                    prospantag = protextdiv.find_element_by_tag_name(
                        'span').text
                    attdic = dict(title=prospantag)
                    allattri[skutitle].append(attdic)
                except TimeoutException:
                    print("time out 202010291049266")
                except NoSuchElementException:
                    print("not find 202010291049268")
        if mainimage==None:
            if otherimglist[0]!=None:
                mainimage=otherimglist[0]
        fulldata = dict(title=title, heightprice=heightprice, lowprice=lowprice, mainimg=mainimage, sku=oursku, allattribute=allattri, otherimg=otherimglist, url=purl, specialtxt=specialtxt,detailhtml=detailhtml)
        logger.info(fulldata)
        # print(fulldata)
        # self.browser.close()
        return fulldata

    def getOimages(self):
        oimage = []
        try:
            oimgul = self.browser.find_element_by_class_name(
                'images-view-list')
            self.browser.execute_script("arguments[0].scrollIntoView();", oimgul)    
            lis = oimgul.find_elements_by_tag_name('li')
            for litem in lis:
                self.browser.execute_script("arguments[0].scrollIntoView();", litem)
                action = ActionChains(self.browser)
                action.move_to_element(litem).click().perform()
                litem.click()
                self.browser.implicitly_wait(5)
                oimgurl = self.getMainimgurl()
                oimage.append(oimgurl)
        except NoSuchElementException:
            print("not find other image 2020111609290930")
            return None
        return oimage
    # 获取产品页的主图

    def getMainimgurl(self):
        try:
            mainimg = self.browser.find_element_by_class_name(
                'magnifier-image')
            self.browser.execute_script("arguments[0].scrollIntoView();", mainimg)     
            return mainimg.get_attribute("src")
        except TimeoutException:
            print("mainimg time out 202010291047276")
            return None
        except NoSuchElementException:
            print("not find 202010291047278")
            return None
    # 关闭iframe中的广告

    def closeiframead(self):
        seq = self.browser.find_elements_by_tag_name('iframe')
        # print(len(seq))
        for index in range(len(seq)):
            try:
                self.browser.switch_to.default_content()
                iframe = self.browser.find_elements_by_tag_name('iframe')[
                    index]
                # name=iframe.get_attribute("name")

                self.browser.switch_to.frame(iframe)
                self.clickAdifram()
            except IndexError:
                print("iframe has been close 202011051030319")
        self.browser.switch_to.default_content()
    # 处理文件
    def handleitembyfile(self, file,resultfile):
        if(not os.path.exists(file)):
            raise Exception('file not exist')
        listres = self.readcsv(file)  # 读取csv
        if not listres:
            raise Exception('file empty')
        # 循环遍历数组
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.writeheader(resultfile)
        for i in listres:
            if re.match(regex, i) is not None:
                pdata = self.getproductdetail(i)
                self.writeInfocsv(pdata,resultfile)
            else:
                continue
    # 写入csv第一行

    def writeheader(self,resultfile):
        f = open(resultfile, 'w', encoding='utf-8-sig', newline='')
        with f:
            fnames = ['product name', 'product_txt_descript', 'high price', 'low price', 'main image', 'url','variation_theme', 'variation_value',
                      'Parentage', 'item_sku', 'Parent SKU', 'image 1', 'image 2', 'image 3', 'image 4', 'image 5', 'image 6', 'image 7', 'image 8','detailhtml']
            writer = csv.DictWriter(f, fieldnames=fnames)

            writer.writeheader()
    
    # 把产品数据写入csv
    def writeInfocsv(self, data,resultfile):
        with open(resultfile, 'a', encoding='utf-8-sig', newline='') as fd:
            # fnames = ['product name', 'product_txt_descript','log price','high price','main image','variation_theme','Parentage','item_sku','Parent SKU','image 1','image 2','image 3','image 4','image 5','image 6','image 7','image 8']
            # writer = csv.DictWriter(fd, fieldnames=fnames)
            # writer.writeheader()

            title = data.get('title')
            allattribute = data.get('allattribute')
            heightprice = data.get('heightprice')
            lowprice = data.get('lowprice')
            mainimg = data.get('mainimg')
            parentsku = data.get('sku')
            otherimg = data.get('otherimg')
            specialtxt=data.get('specialtxt')
            url=data.get('url')
            detailhtml=data.get('detailhtml')
            attlist = []
            attrikeys = list(allattribute.keys())
            for akeyo in attrikeys:
                avavarr = allattribute.get(akeyo)
                for akey in avavarr:
                    if isinstance(akey, dict):
                        attrval = akey.get('title')
                        aitem = dict(attribute_name=akeyo,
                                     attribute_value=attrval)
                        aimage = akey.get('image')
                        if aimage != None:
                            aitem['attribute_image'] = aimage
                        else:
                            aitem['attribute_image'] = None
                        attlist.append(aitem)

            comfieldnames = ['product_name', 'product_txt_descript', 'high_price', 'low_price', 'main_image', 'url','variation_theme', 'variation_value',
                             'parentage', 'item_sku', 'parent_sku', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'image_8','detailhtml']
            # 写入主属性
            writer = csv.DictWriter(fd, fieldnames=comfieldnames)
            parendvale = dict(product_name=title, product_txt_descript=specialtxt, high_price=heightprice, low_price=lowprice,
                              main_image=mainimg, url=url,variation_theme=None, parentage=None, item_sku=None, parent_sku=parentsku,detailhtml=detailhtml)

            for x in range(0, len(otherimg)):
                if x < 8:
                    parendvale['image_'+str(int(x)+1)] = otherimg[x]

            writer.writerow(parendvale)
            # 开始循环属性
            si = 1
            for sitem in attlist:
                childsku = parentsku+"_"+str(si)
                childvale = dict(product_name=title, product_txt_descript=specialtxt, high_price=heightprice, low_price=lowprice,
                                 main_image=mainimg, url=url,variation_theme=None, parentage=None, item_sku=childsku, parent_sku=parentsku)
                childvale['variation_theme'] = sitem.get('attribute_name')
                childvale['variation_value'] = sitem.get('attribute_value')
                mainimg = sitem.get('attribute_image')
                if mainimg != None:
                    childvale['main_image'] = mainimg
                si += 1
                for x in range(0, len(otherimg)):
                    if x < 8:
                        childvale['image_'+str(int(x)+1)] = otherimg[x]
                writer.writerow(childvale)

                # if isinstance(avav,dict):

            # writer.writerow({'first_name' : 'John', 'last_name': 'Smith'})
