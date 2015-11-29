# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from re import split

from CityResearch.items import CityresearchItem
class WanfangSpider(Spider):
    name = "wanfang"
    allowed_domains = [
        "d.wanfangdata.com.cn",
        "s.wanfangdata.com.cn"
    ]
    start_urls = [
        'http://s.wanfangdata.com.cn/Paper.aspx?q=关键词%3A碳排放&f=top'
    ]

    def parse(self, response):
        print 'hhahaha'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="record-item"]//div[@class="record-title"]/a[@class="title"]/@href')
        
        paperinfo=sites.extract()
     
        for i in paperinfo:
            yield Request(i,callback=self.parse_paperinfo)
        
    def parse_paperinfo(self,response):
        sel = Selector(response)
        item=CityresearchItem()
        baseinfo=sel.xpath('//div[@class="section-baseinfo"]')      
        tmp=baseinfo.xpath('h1/text()').extract()[0].encode('utf-8')
        item['name_Chinese']=split("\r\n",tmp)[0]
        item['name_English']=baseinfo.xpath('h2/text()').extract()
        ### Maybe abstract informations are useless
        # item['abstract_Chinese'] = baseinfo.xpath('//div[@class="text"]/text()').extract()
        # item['abstract_English'] = baseinfo.xpath('//div[@class="text"]/text()').extract()

        baseinfofd=sel.xpath('//div[@class="fixed-width-wrap fixed-width-wrap-feild"]//div[@class="fixed-width baseinfo-feild"]')
        # print baseinfofd.extract()

        #Information dictionary for data organization
        listnumdict ={'doi':0,'作者':1,'Author':2,'作者单位':3,'刊  名':4,
                'Journal':5,'年，卷(期)':6,'分类号':7,'关键词':8,'Keywords':9,'机标分类号':10,
                '在线出版日期':11,'基金项目':12
        }
        itemdict={0:'doi',1:'authors_Chinese',2:'authors_English',3:'institutions',4:'journal_Chinese',
        5:'journal_English',6:'volume',7:'classify_code',8:'keywords_Chinese',9:'keywords_English',10:'machineclassify_code',
        11:'date',12:'fundings'
        }
     
        PreList=[]
        for i in range(1,len(baseinfofd.xpath('div'))+1):
            #extract the pre word (e.g."doi:"), remove ':' then add it into Pre words List
            tmp=(baseinfofd.xpath('div['+str(i)+']'+'/span[@class="pre"]/text()').extract())[0][:-1].encode('utf-8')
            PreList.append(tmp)
            n=listnumdict[tmp]
            with_a=[0,4,5,6]
            without_a=[7,10,11,12]
            r_inst=[3]
            r_author=[1,2]
            r_kw=[8,9]
            if n in with_a:
                item[itemdict[n]]=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]/a/text()').extract()[0].encode('utf-8')
            elif n in without_a:
                item[itemdict[n]]=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]/text()').extract()[0].encode('utf-8')
            elif n in r_inst:

                Inlist=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]')
                # Remove '\r\n' and leading and ending space 
                def remove(strinst):
                    tmp=strinst.replace("\r\n","")
                    re=tmp.strip()
                    return re
                
                nspan=len(Inlist.xpath('span'))
                # In case of unique institution 
                if nspan==0:
                    # Data type should be list for consistency
                    tmp=Inlist.xpath('text()').extract()[0]                    
                    item[itemdict[n]]=[remove(tmp).encode('utf-8')]
                # In case of multiple institutions  
                else:
                    Instlist=[]
                    for j in range(1,nspan+1):
                        tmp=Inlist.xpath('span['+str(j)+']/text()').extract()[0].encode('utf-8')
                        Instlist.append(tmp)
                    item[itemdict[n]]=Instlist
            elif n in r_author:
                row_author=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]')
                namelist=[]

                #In case of authors_Chinese
                if n==1:# with links to authors' homepages
                    hmplist=[]
                    for i in range(1,len(row_author.xpath('a'))+1):                        
                        namelist.append(row_author.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8'))
                        hmplist.append(row_author.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))
                    namelist=[namelist,hmplist]

                #In case of authors_English
                else:
                    for i in range(1,len(row_author.xpath('span'))+1):
                        namelist.append(row_author.xpath('span['+str(i)+']/text()').extract()[0].encode('utf-8'))
                
                item[itemdict[n]]=namelist            
            elif n in r_kw:
                row_keyword=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]')
                # In case of keywords_Chinese
                if n==8:
                    kwlist=[]
                    hmplist=[]
                    trendlist=[]
                    for i in range(1,len(row_keyword.xpath('a'))+1):                                                
                        if i%2==1:
                            kwlist.append(row_keyword.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8'))
                            hmplist.append(row_keyword.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))
                        else:                                          
                            trendlist.append(row_keyword.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))
                    kw=[[kwlist,hmplist],trendlist]
                # In case of keywords_English       
                else:
                    kwlist=[]
                    hmplist=[]
                    for i in range(1,len(row_keyword.xpath('a'))+1):                        
                        kwlist.append(row_keyword.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8'))
                        hmplist.append(row_keyword.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))

                        
                    
                    kw=[kwlist,hmplist]
                item[itemdict[n]]=kw                
            else:
                print 'there is some exception for item mapping'            

        return item
