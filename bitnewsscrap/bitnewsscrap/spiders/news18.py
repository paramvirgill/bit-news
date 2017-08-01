import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2


class News18Spider(CrawlSpider):
    name = "news18-india"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/india.xml",
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

class News18Spider1(CrawlSpider):
    name = "news18-world"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/world.xml",
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

class News18Spider2(CrawlSpider):
    name = "news18-business"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/business.xml",
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

class News18Spider3(CrawlSpider):
    name = "news18-tech"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/tech.xml",
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

class News18Spider4(CrawlSpider):
    name = "news18-sports"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/sports.xml",
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

class News18Spider5(CrawlSpider):
    name = "news18-lifestyle"
    allowed_domains = ["news18.com"]
    start_urls = [
                    "http://www.news18.com/rss/lifestyle.xml",
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