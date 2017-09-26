from scrapy.spiders import Spider
from scrapy1.items import scrapy1Item
from scrapy.http    import Request
import re
 
class MySpider(Spider):
  name = "scrapy1"
  allowed_domains   = ["code.tutsplus.com"]
  start_urls = ["http://code.tutsplus.com/"]
 
  def parse(self, response):
    links = response.xpath('//a/@href').extract()
 
    # We stored already crawled links in this list
    crawledLinks = []
 
    # Pattern to check proper link
    # I only want to get the tutorial posts
    linkPattern = re.compile("^\/tutorials\?page=\d+")
 
    for link in links:
      # If it is a proper link and is not checked yet, yield it to the Spider
      if linkPattern.match(link) and not link in crawledLinks:
        link = "http://code.tutsplus.com" + link
        crawledLinks.append(link)
        yield Request(link, self.parse)
 
    titles = response.xpath('//a[contains(@class, "posts__post-title")]/h1/text()').extract()
    for title in titles:
      item = scrapy1Item()
      item["title"] = title
      yield item