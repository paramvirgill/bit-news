import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2

class OneindiaSpider(CrawlSpider):
	name = "oneindia-telugu"
	allowed_domains = ["telugu.oneindia.com"]
	start_urls = (
		'http://telugu.oneindia.com/rss/telugu-news-fb.xml',
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
		item['image'] = response.xpath("//*[@class='big_center_img']/@*[4]").extract()
		yield item


class OneindiaSpider1(CrawlSpider):
	name = "oneindia-tamil"
	allowed_domains = ["tamil.oneindia.com"]
	start_urls = (
		'http://tamil.oneindia.com/rss/tamil-news-fb.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubDate/text()").extract()
			item['image']=title.xpath("enclosure/@*[1]").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image2'] = response.xpath("//*[@class='big_center_img']/@*[4]").extract()
		yield item


class OneindiaSpider2(CrawlSpider):
	name = "oneindia-kannada"
	allowed_domains = ["kannada.oneindia.com"]
	start_urls = (
		'http://kannada.oneindia.com/rss/kannada-news-fb.xml',
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
		item['image'] = response.xpath("//*[@class='imgClSlider']/img/@*[1]").extract()
		yield item