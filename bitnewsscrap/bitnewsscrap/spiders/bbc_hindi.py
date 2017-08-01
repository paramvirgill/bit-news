import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector, HtmlXPathSelector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2


class MySpider(CrawlSpider):
    name = "toi-india"
    allowed_domains = ["timesofindia.indiatimes.com"]
    start_urls = [
                    "http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

# //*[@id="top-stories"]/div/div[1]/h3/a