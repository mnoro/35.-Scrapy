# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
# from jdcal import gcal2jd, jd2gcal

### Def

import numpy as np 
import pandas as pd 
import os
import random
pathInput = './data'
### Setting parameters
# Google Hacks:
'''
    Google Hacks
    ============

            intitle: restrict search to web pages title

            inurl: restrict search to the URLs of the web pages
                allinurl:

            intext: serch only body text (ignores link text URL and titles)

            link:  returns a list of pages that link to the specified URL

            cache: find a copy of the page even if not available at the original URL

            daterange: using Julian dates e.g. "George Bus' daterange:2452389-2452389

            after: after a specific date, like after:2020-05-01

            before: similar to after

            filetype: searches the suffixes or filenames extension

            related: finds pages relatd to the specific one

            location: to indicate

    Possible problems running Scrapy on Windows machine
    ===================================================
            Within a company, firewalls may present an obstacle to Scrapy
            In order to have it run, from the command prompt (Window) please
            set the following env variables:

                set https_proxy=https://lobluecoatp1001.nomura.com:80
                set http_proxy=http://lobluecoatp1001.nomura.com:80
'''


search_string = ''

class Google003_Spider(scrapy.Spider):
    name = 'google_003'
    # allowed_domains = ['google.com']
    start_urls = ['https://google.com/']
    # Interesting search engines
    #   1. google.com
    #   2. news.google.com
    base_url='https://www.google.com'
    search_string0='search?q=' #+'fiat+after:2020-05-01+inurl:finance.yahoo.com+fraud+OR+probe'

# Reads in Negative keywords (there's a limit to 32 words as per Google)
    df = pd.read_csv(os.path.join(pathInput, 'negativeKeywords.csv'))
    negativeKeywords = list(df['NegativeKeyword'])
    negativeKeywords = [str('"'+x+'"') for x in negativeKeywords]

# Reads in the Counterparties
    df = pd.read_csv(os.path.join(pathInput, 'cp_test.csv'))
    counterparties = list(df['Counterparty'])
    # counterparties = counterparties[1:2]
    dateSearch = '2020-01-01'

# Reads in the trusted sites
    df = pd.read_csv(os.path.join(pathInput, 'sites_test.csv'))
    site2search = list(df['sitename'])
    site2search = [x for x in site2search]
    #site2search = site2search[0:1]

    #Build search String
    neg = '+OR+'.join(negativeKeywords)
    cp = '"'+'+OR+'.join(counterparties)+'"'
    sites = '+OR+'.join(site2search)
    # ss contains the list of searches built this way
    # for each cp
    #   for each inurl
    #     for all the keywords
    ss = []
    pattern = 'search?q=%s+after:%s+inurl:%s+%s'
    currentCpSiteLst = []
    for c in counterparties:
        for s in site2search:
            ss.append(pattern %('"'+c+'"',dateSearch,s,neg))
            currentCpSiteLst.append(c+"|"+s)
    currentCpSite=''
    # ss = random.sample(ss, 15)
    print("\n\nNumber of sites: %s"%(len(ss)))
    # ss = ['search?q=fiat+after:2020-05-01+inurl:finance.yahoo.com+fraud',
    #     'search?q=fiat+after:2020-05-01+inurl:theguardian.com+fraud+OR+probe']

    search_string = search_string0 + cp +"+"+dateSearch+"+"+sites+"+"+neg
    tmpDf = pd.DataFrame()
    tmpDf.loc[0,'SearchString']=search_string
    tmpDf.to_csv('./data/searchstring.csv')
    pageCounter=0
    pageLimit=4  # Number of pages to retrieve 
    pageHtml = ''

    def start_requests(self):
        '''
            The start of the requests.
            One request per Url
        '''
        # this is executed at the start of the search
        # df = pd.read_csv(os.path.join(pathInput,'searches.csv'))
        print("\nSearch String: %s"%(self.search_string))
        # The number of searches are executed one after the other
        # iterating over the list and yielding each request
        for z in self.ss:
            # The site and counterparties parameters are passed through
            # self.variables
            currentCpSite = self.currentCpSiteLst[self.ss.index(z)]
            yield scrapy.Request(url =self.start_urls[0]+z,
                callback = self.parse, 
                meta={'cp':currentCpSite.split("|")[0], 'site':currentCpSite.split("|")[1]},
                headers = {
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                    }
            )
    def retrievePage(self, url):
        yield scrapy.Request(url =url,
            callback = self.parse_result, 
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                }
        )         

    def parse(self, response):
        print('PAGE %s of Results' % (self.pageCounter+1))
        print(">>>>",response.xpath("//*[@id='topstuff']/div/div/div[1]/text()[1]").get(), "<<<<")
        for entry in response.xpath("//div[@class='r']"):
            # Extracts data from the search results
            url = entry.xpath(".//a/@href").get()
            data = requests.get(url)
            soup = BeautifulSoup(data.text,"lxml")
            yield{
                'counterParty': response.meta['cp'],
                'site': response.meta['site'],
                'dateSearch': 'after:'+self.dateSearch,
                'searchText': response.url,
                'pageCount': self.pageCounter,
                'urlResult': entry.xpath(".//a/@href").get(),
                'titleResult':entry.xpath(".//h3/text()").get(),
                'bodyResult':entry.xpath(".//span[@class='st']/text()").get(),
                # 'pageResultHtml':self.pageHtml,
                'pageResultHtml': soup.get_text(' ',strip=True)
            }
        self.pageCounter += 1
        if self.pageCounter < self.pageLimit:
            next_page = response.xpath("//a[@id='pnnext']/@href").get()
            if next_page is None:
                # Search for omitted results
                next_page = response.xpath("//a[text()='repeat the search with the omitted results included']/@href").get()
            # print(">>>!!%s"%(next_page))
            if next_page is not None:
                next_page = response.urljoin(next_page)
                # print(">>|||||>%s"%(next_page))
                yield scrapy.Request(url = next_page, # Specify URL= ortherwise doesn't worlk
                    callback = self.parse,
                    headers = {
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })
# To parse the page containing the 
    def parse_result(self, response):
        print('Scraping Content')
        self.pageHtml = "HTML Content of Page"
        yield {self.pageHtml}
