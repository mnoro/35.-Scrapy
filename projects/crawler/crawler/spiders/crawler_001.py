# -*- coding: utf-8 -*-
import scrapy


class Crawler001Spider(scrapy.Spider):
    name = 'crawler_001'
    allowed_domains = ['google.com']
    start_urls = ['https://google.com/search?q=fiat+after:2020-05-01+inurl:finance.yahoo.com+fraud+OR+probe',
                'https://google.com/search?q=apple+after:2020-05-01+inurl:finance.yahoo.com+fraud+OR+probe']

    pageCounter=0
    pageLimit=4
    pageHtml = ''

    def retrievePage(self, url):
        yield scrapy.Request(url =url,
            callback = self.parse_result, 
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                }
        )         

    def parse(self, response):
        print('PAGE %s of Results' % (self.pageCounter+1))
        for entry in response.xpath("//div[@class='r']"):
            # Extracts data from the search results
            url = entry.xpath(".//a/@href").get()
            data = requests.get(url)
            soup = BeautifulSoup(data.text,"lxml")
            yield{
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