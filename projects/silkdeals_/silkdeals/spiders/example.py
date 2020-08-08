# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']
    def start_request(self):
        yield SeleniumRequest(
            url = 'https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # pass
        print('Parsing Page')
        img = response.request.meta['screenshot']
        with open('screenshot.png', 'wb') as f:
            f.write(img)
            print('Writing to file...')
            f.close()
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepge']")
        search_input.send_keys("Hello World")
        driver.save_screenshot('after_Filling_input.png')

