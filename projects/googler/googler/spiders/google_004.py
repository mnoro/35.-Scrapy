# -*- coding: utf-8 -*-
import scrapy


class Google004Spider(scrapy.Spider):
    name = 'google_004'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass
