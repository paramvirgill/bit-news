# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2


class ZeenewsSpider(CrawlSpider):
	name = "zee-india"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/india-national-news.xml',
	)

	def parse(self, response):
		items=[]
		titles = response.selector.xpath("//item")
		for title in titles:
			item = BitnewsscrapItem2()
			item['title'] = title.xpath("title/text()").extract()
			item['description'] = title.xpath("description/text()").extract()
			item['pubdate'] = title.xpath("pubdate/text()").extract()
			item['link'] = title.xpath("link/text()").extract()
			for x in item['link']:
				if item['link']:
                			item['link'] = response.urljoin(x)
            		yield Request(item['link'], meta={'item': item},callback=self.parse_images)
  			items.append(item)

	def parse_images(self, response):
		item = response.request.meta['item']
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item


class ZeenewsSpider1(CrawlSpider):
	name = "zee-world"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/world-news.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item

class ZeenewsSpider2(CrawlSpider):
	name = "zee-business"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/business.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item

class ZeenewsSpider3(CrawlSpider):
	name = "zee-sports"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/sports-news.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item

class ZeenewsSpider4(CrawlSpider):
	name = "zee-tech"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/science-technology-news.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item

class ZeenewsSpider5(CrawlSpider):
	name = "zee-entertainment"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/rss/entertainment-news.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[3]").extract()
		yield item

##########################ZEE BENGALI#######################################
class ZeenewsSpider6(CrawlSpider):
	name = "zee-bengali-india"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/bengali/rssfeed/nation.xml',
		'http://zeenews.india.com/bengali/rssfeed/kolkata.xml'
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[2]").extract()
		yield item


class ZeenewsSpider7(CrawlSpider):
	name = "zee-bengali-world"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/bengali/rssfeed/world.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[2]").extract()
		yield item


class ZeenewsSpider8(CrawlSpider):
	name = "zee-bengali-sports"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/bengali/rssfeed/sports.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[2]").extract()
		yield item


class ZeenewsSpider9(CrawlSpider):
	name = "zee-bengali-entertainment"
	allowed_domains = ["zeenews.india.com"]
	start_urls = (
		'http://zeenews.india.com/bengali/rssfeed/entertainment.xml',
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
		item['image'] = response.xpath("//*[@class='article-image']/div/div/div/img/@*[2]").extract()
		yield item

