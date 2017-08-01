import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2

class ThestarSpider(CrawlSpider):
    name = "thestar-india"
    allowed_domains = ["thestar.com"]
    start_urls = [
                    "http://www.thestar.com.my/rss/editors-choice/nation/",
                    "http://www.thestar.com.my/rss/news/nation/"
                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem2()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['image'] = title.xpath("enclosure/@*[1]").extract()
            if not item['image']:
            	continue
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

class ThestarSpider1(CrawlSpider):
    name = "thestar-world"
    allowed_domains = ["thestar.com"]
    start_urls = [
                    "http://www.thestar.com.my/rss/news/world/",
                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem2()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['image'] = title.xpath("enclosure/@*[1]").extract()
            if not item['image']:
            	continue
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

class ThestarSpider2(CrawlSpider):
    name = "thestar-education"
    allowed_domains = ["thestar.com"]
    start_urls = [
                    "http://www.thestar.com.my/rss/news/education/",
                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem2()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['image'] = title.xpath("enclosure/@*[1]").extract()
            if not item['image']:
            	continue
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

class ThestarSpider3(CrawlSpider):
    name = "thestar-business"
    allowed_domains = ["thestar.com"]
    start_urls = [
                    "http://www.thestar.com.my/rss/editors-choice/business/",

                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem2()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['image'] = title.xpath("enclosure/@*[1]").extract()
            if not item['image']:
            	continue
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

class ThestarSpider4(CrawlSpider):
    name = "thestar-sports"
    allowed_domains = ["thestar.com"]
    start_urls = [
                    "http://www.thestar.com.my/rss/editors-choice/sport/",
                ]

    def parse(self, response):
        items=[]
        titles = response.selector.xpath("//item")
        for title in titles:
            item = BitnewsscrapItem2()
            item['title'] = title.xpath("title/text()").extract()
            item['description'] = title.xpath("description/text()").extract()
            item['link'] = title.xpath("link/text()").extract()
            item['image'] = title.xpath("enclosure/@*[1]").extract()
            if not item['image']:
            	continue
            item['pubdate'] = title.xpath("pubDate/text()").extract()
            items.append(item)
        return items

