# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import os

class Google01Spider(CrawlSpider):
    name = 'google_01'
    allowed_domains = ['google.com']
    search_string='search?rlz=2C5CHFA_enGB0537GB0851&ei=MmcTX43lA_iFhbIPu4-d6AU&q=golders+green&oq=golders+green&gs_lcp=CgZwc3ktYWIQAzIKCC4QsQMQQxCTAjICCAAyAggAMgoILhDHARCvARBDMggILhDHARCvATIICC4QxwEQrwEyCAguEMcBEK8BMggILhDHARCvATICCAAyBAgAEEM6BAgAEEc6BwguEEMQkwI6BAgAEAo6CgguEMcBEK8BEApQnBtY3R9g2CJoAHABeACAAXKIAeMBkgEDMC4ymAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiNxo6L3dfqAhX4QkEAHbtHB10Q4dUDCAw&uact=5'
    start_urls = ['https://google.com/'+search_string]
    counter = 0
    
    rules = (
        # Rule(LinkExtractor(restrict_xpaths="//div[@class='r']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='r']/a/@href"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@id="pnnext"]/@href')),
    )

    # def __init__(self):
    #     chrome_options = Options()
    #     # chrome_options.add_argument("--headless") # for debug comment out
    #     # chrome_path = which("chromedriver")
    #     # chrome_path
    #     # chrome_path = "chromedriver"
    #     # driver=webdriver.Chrome(executable_path=r"./chromedriver",
    #     #         options=chrome_options)
    #     driver = webdriver.Chrome(executable_path=r"./chromedriver")
    #     driver.get(self.start_urls[0])

    #     search_input = driver.find_element_by_xpath("//input[@type='text']")
    #     search_input.send_keys("Golders Green")

    #     # search_btn= driver.find_element_by_xpath("//input[@id='search_button_homepage']")
    #     # search_btn.click()
    #     search_input.send_keys(Keys.ENTER)
    #     self.html=driver.page_source
    #     print(self.html)
    #     driver.close()

    def parse_item(self, response):
        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        # resp = Selector(self.html)
        # for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
        #     yield {
        #         'currency pair': currency.xpath(".//div[1]/div/text()").get(),
        #         'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
        #     }
        self.counter +=1
        print('Counter %d' %(self.counter))
        if self.counter > 100:
            exit
        yield{

            'url': entry.xpath(".//a/@href").get(),
            'title':entry.xpath(".//h3/text()").get(),
            'body':entry.xpath(".//span[@class='st']/text()").get(),
        }

