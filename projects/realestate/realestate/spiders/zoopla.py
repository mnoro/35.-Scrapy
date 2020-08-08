# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class ZooplaSpider(CrawlSpider):
    name = 'zoopla'
    allowed_domains = ['zoopla.com']
    start_urls = ['http://zoopla.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_path = which("chromedriver")
        chrome_path
        # chrome_path = "chromedriver"
        # driver=webdriver.Chrome(executable_path=r"./chromedriver",
        #         options=chrome_options)
        driver = webdriver.Chrome(executable_path=r"./chromedriver")
        driver.get(self.start_urls[1])

        rur_tab = driver.find_elements_by_xpath('//div[starts-with(@class,"filterPanelItem")]')
        rur_tab[4].click()
        self.html=driver.page_source
        driver.close()

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
