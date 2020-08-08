# -*- coding: utf-8 -*-
import scrapy


class WorldpopreviewSpider(scrapy.Spider):
    name = 'worldpopreview'
    allowed_domains = ['https://worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        # pass
        rows = response.xpath("//table[@class='datatableStyles__StyledTable-ysgkm4-1 dXImya table table-striped']/tbody/tr")
        for row in rows:
            country = row.xpath("./td[1]/a/text()").get()
            nationalDebt2GDP = row.xpath("./td[2]/text()").get()
            population = row.xpath("./td[3]/text()").get()
            yield {
                'country': country,
                'nationalDebt2GDP' : nationalDebt2GDP,
                'population':population
            }