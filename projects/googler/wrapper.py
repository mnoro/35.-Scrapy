import scrapy
import sys

from googler.spiders.google_003 import Google003_Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

settings = get_project_settings()
crawler = CrawlerProcess(settings)

crawler.crawl(Google003_Spider,[])