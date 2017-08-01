import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2

class IbnliveSpider(CrawlSpider):
	name = "ibnlive-india"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/desh/desh.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='myImage']/@*[3]").extract()
		yield item

class IbnliveSpider1(CrawlSpider):
	name = "ibnlive-sports"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/khel/khel.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/div[1]/figure/img/@*[1]").extract()
		yield item

class IbnliveSpider2(CrawlSpider):
	name = "ibnlive-cricket"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/khel/cricket.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		yield item

class IbnliveSpider3(CrawlSpider):
	name = "ibnlive-business"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/karobar/karobar.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		yield item

class IbnliveSpider4(CrawlSpider):
	name = "ibnlive-entertainment"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/manoranjan/manoranjan.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		yield item


class IbnliveSpider5(CrawlSpider):
	name = "ibnlive-tech"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/lifestyle/gadgets.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		yield item

class IbnliveSpider6(CrawlSpider):
	name = "ibnlive-lifestyle"
	allowed_domains = ["khabar.ibnlive.com"]
	start_urls = (
		'http://khabar.ibnlive.com/rss/khabar/lifestyle/lifestyle.xml',
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
		item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		if not item['image']:
			item['image'] = response.xpath("//*[@id='blog_contener']/article/figure/img/@*[1]").extract()
		yield item

