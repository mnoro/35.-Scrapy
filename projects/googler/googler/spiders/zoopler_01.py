# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup

class Zoopler01Spider(scrapy.Spider):
    name = 'zoopler_01'
    allowed_domains = ['zoopla.co.uk']
    start_urls = ['https://www.zoopla.co.uk/']
    search_string='for-sale/property/golders-green/?q=Golders%20Green%2C%20London'
    pageCounter=0
    pageLimit=5
    pageHtml = ''

    def start_requests(self):
        yield scrapy.Request(url =self.start_urls[0]+self.search_string,
            callback = self.parse, 
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
        for entry in response.xpath("//li[@class='srp clearfix   ']"):
            # Extracts data from the search results
            url = entry.xpath(".//a/@href").get()
            data = requests.get(url)
            soup = BeautifulSoup(data.text,"lxml")
            yield{
                'pageCount': self.pageCounter,
                'Price': entry.xpath(".//a[@class='listing-results-price text-price']").get(),
                'urlResult': entry.xpath(".//a/@href").get(),
                'Address': entry.xpath(".//a[@class='listing-results-address']/text()").get(),
                'bodyResult':entry.xpath(".//span[@class='st']/text()").get(),
                'ListedBy': entry.xpath().get(".//div[@class='listing-results-left']"),
                # 'pageResultHtml':self.pageHtml,
                'pageResultHtml': soup.get_text(' ',strip=True)
            }
        self.pageCounter += 1
        if self.pageCounter < self.pageLimit:
            next_page = response.xpath("//div[@class='paginate bg-muted']/a/@href").get()
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

    def parse(self, response):
        pass
