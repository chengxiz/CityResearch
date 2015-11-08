# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
import re
import scrapy
from CityResearch.items import CityresearchItem
class WanfangSpider(Spider):
    name = "wanfang"
    allowed_domains = [
        "d.wanfangdata.com.cn",
        "s.wanfangdata.com.cn"
    ]
    start_urls = [
        'http://s.wanfangdata.com.cn/Paper.aspx?q=关键词%3A碳循环&f=top'
    ]

    def parse(self, response):
        print 'hhahaha'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="record-item"]//div[@class="record-title"]/a[@class="title"]/@href')
        
        paperinfo=sites.extract()
     
        for i in paperinfo:
            yield scrapy.Request(i,callback=self.parse_paperinfo)
        
    def parse_paperinfo(self,response):
        sel = Selector(response)
        item=CityresearchItem()
        baseinfo=sel.xpath('//div[@class="section-baseinfo"]')      
        tmp=baseinfo.xpath('h1/text()').extract()[0].encode('utf-8')
        item['name_Chinese']=re.split("\r\n",tmp)[0]
        item['name_English']=baseinfo.xpath('h2/text()').extract()
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

        # print baseinfofd.xpath('div[@class="row row-author"]/span[@class="text"]').extract()
        # print 'what'
        # print baseinfofd.xpath('div[1]').extract()
        # print 'the HELL'
        # print 'the number of properties is '+str(len(baseinfofd.xpath('div')))
        PreList=[]
        for i in range(1,len(baseinfofd.xpath('div'))+1):
            #extract the pre word (e.g."doi:"), remove ':' then add it into Pre words List
            # print 'div['+str(i+1)+']'+'/span[@class="pre"]/text()'
            tmp=(baseinfofd.xpath('div['+str(i)+']'+'/span[@class="pre"]/text()').extract())[0][:-1].encode('utf-8')
            print tmp
            PreList.append(tmp)
            n=listnumdict[tmp]
            with_a=[0,4,5,6]
            without_a=[3,7,10,11,12]
            r_author=[1,2]
            r_kw=[8,9]
            if n in with_a:
                print n
                item[itemdict[n]]=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]/a/text()').extract()[0].encode('utf-8')
            elif n in without_a:
                print n
                item[itemdict[n]]=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]/text()').extract()[0].encode('utf-8')
            
            elif n in r_author:
                row_author=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]')
                namelist=[]


# woCAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# this way is designed for 
# [1] "X-Ray Fluorescence Spectrum Studies on Bioorganic Carbon in Cereals and Carbon Chemical Circulation"
# not for 
# Study on the Creation of the Regional Carbon Cycle Pressure Index Model and Its Regulation Mechanism"

# they use two reverse ways to organize (ENgish/CHinese)

                #In authors_Chinese case
                if n==1:# with links to authors' homepages
                    hmplist=[]
                    for i in range(1,len(row_author.xpath('a'))+1):
                        print 'the length is'
                        print len(row_author.xpath('a'))
                        print i
                        namelist.append(row_author.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8'))
                        hmplist.append(row_author.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))
                    namelist=[namelist,hmplist]

                #In authors_English case
                else:
                    for i in range(1,len(row_author.xpath('span'))+1):
                        namelist.append(row_author.xpath('span['+str(i)+']/text()').extract()[0].encode('utf-8'))
                
                item[itemdict[n]]=namelist            
            elif n in r_kw:
                row_keyword=baseinfofd.xpath('div['+str(i)+']/span[@class="text"]')
                # In keywords_Chinese case
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
                # In keywords_English case                
                else:
                    kwlist=[]
                    hmplist=[]
                    print row_keyword.extract()
                    print 'len is' 
                    print len(row_keyword.xpath('a'))
                    for i in range(1,len(row_keyword.xpath('a'))+1):                        
                        kwlist.append(row_keyword.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8'))
                        print row_keyword.xpath('a['+str(i)+']/text()').extract()[0].encode('utf-8')
                        print i
                        hmplist.append(row_keyword.xpath('a['+str(i)+']/@href').extract()[0].encode('utf-8'))

                        
                    print 'English Keywords are'
                    
                    kw=[kwlist,hmplist]
                item[itemdict[n]]=kw                
            else:
                print 'there is some exception for item mapping'            
        # print PreList
        # print str(listnumdict[PreList[0]])+'that is '
        
        # 1 ## item['doi'] = baseinfofd.xpath('div[1]/span[@class="text"]/a/text()').extract()
        # 2 ## item['authors_Chinese'] = baseinfofd.xpath('div[2]/span[@class="text"]/a/text()').extract()
        # 3 ## item['authors_English'] = baseinfofd.xpath('div[3]/span[@class="text"]/a/text()').extract()

        # 4 ## item['institutions'] = baseinfofd.xpath('div[4]/span[@class="text"]/text()').extract()
        # 5 ## item['journal_Chinese'] = baseinfofd.xpath('div[5]/span[@class="text"]/a/text()').extract()
        # 6 ## item['journal_English'] = baseinfofd.xpath('div[6]/span[@class="text"]/a/text()').extract()
        # 7 ## item['volume'] = baseinfofd.xpath('div[7]/span[@class="text"]/a/text()').extract()
        # 8 ## item['classify_code'] = baseinfofd.xpath('div[8]/span[@class="text"]/text()').extract()
        # 9 ## item['keywords'] = baseinfofd.xpath('div[9]/span[@class="text"]/a/text()').extract()
        # 10 ## item['machineclassify_code'] = baseinfofd.xpath('div[10]/span[@class="text"]/text()').extract()
        # 11 ## item['date']= baseinfofd.xpath('div[11]/span[@class="text"]/text()').extract()
        # 12 ## item['fundings'] = baseinfofd.xpath('div[12]/span[@class="text"]/text()').extract()
        return item
