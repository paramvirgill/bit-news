import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2

class AmarujalaSpider(CrawlSpider):
	name = "amarujala-india"
	allowed_domains = ["www.amarujala.com"]
	start_urls = (
		'http://www.amarujala.com/rss/india.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@id='body']/div[3]/div/div[1]/div[2]/img/@*[2]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item

class AmarujalaSpider1(CrawlSpider):
	name = "amarujala-sports"
	allowed_domains = ["www.amarujala.com"]
	start_urls = (
		'http://www.amarujala.com/rss/sports-news.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@id='body']/div[3]/div/div[1]/div[2]/img/@*[2]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item

class AmarujalaSpider2(CrawlSpider):
	name = "amarujala-business"
	allowed_domains = ["www.amarujala.com"]
	start_urls = (
		'http://www.amarujala.com/rss/business.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@id='body']/div[3]/div/div[1]/div[2]/img/@*[2]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item

class AmarujalaSpider3(CrawlSpider):
	name = "amarujala-tech"
	allowed_domains = ["www.amarujala.com"]
	start_urls = (
		'http://www.amarujala.com/rss/technology-news.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@id='body']/div[3]/div/div[1]/div[2]/img/@*[2]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item

class AmarujalaSpider4(CrawlSpider):
	name = "amarujala-lifestyle"
	allowed_domains = ["www.amarujala.com"]
	start_urls = (
		'http://www.amarujala.com/rss/lifestyle-news.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@id='body']/div[3]/div/div[1]/div[2]/img/@*[2]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item





