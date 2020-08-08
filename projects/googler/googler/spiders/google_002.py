# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import os

class Google002Spider(scrapy.Spider):
    name = 'google_002'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # for debug comment out
        # chrome_path = which("chromedriver")
        # chrome_path
        # chrome_path = "chromedriver"
        # driver=webdriver.Chrome(executable_path=r"./chromedriver",
        #         options=chrome_options)
        driver = webdriver.Chrome(executable_path=r"./chromedriver")
        driver.get(self.start_urls[0])

        search_input = driver.find_element_by_xpath("//input[@type='text']")
        search_input.send_keys("Golders Green")

        # search_btn= driver.find_element_by_xpath("//input[@id='search_button_homepage']")
        # search_btn.click()
        search_input.send_keys(Keys.ENTER)
        self.html=driver.page_source
        print(self.html)
        driver.close()


    def parse(self, response):
        # pass
        resp = Selector(self.html)
        print(self.html)
        for a_link in resp.xpath("//div[@class='r']"):
            yield {
                'linkUrl': a_link.xpath(".//a/@href").get(),
            }
