from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem


class JagranSpider(CrawlSpider):
    name = "jagran-india"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/news/national.xml",
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

class JagranSpider1(CrawlSpider):
    name = "jagran-world"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/news/world.xml",
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

class JagranSpider2(CrawlSpider):
    name = "jagran-business"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/news/business.xml",
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

class JagranSpider3(CrawlSpider):
    name = "jagran-sports"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/news/sports.xml",
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

class JagranSpider4(CrawlSpider):
    name = "jagran-entertainment"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/entertainment/bollywood.xml",
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

class JagranSpider5(CrawlSpider):
    name = "jagran-cricket"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/cricket/headlines.xml",
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

class JagranSpider6(CrawlSpider):
    name = "jagran-education"
    allowed_domains = ["jagran.com"]
    start_urls = [
                    "http://rss.jagran.com/rss/josh/shiksha.xml",
                    "http://rss.jagran.com/rss/josh/career.xml"
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
