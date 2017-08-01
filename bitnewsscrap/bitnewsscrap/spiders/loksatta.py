import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector, HtmlXPathSelector
from bitnewsscrap.items import BitnewsscrapItem, BitnewsscrapItem2


class DainikSpider(CrawlSpider):
	name = "loksatta"
	allowed_domains = ["loksatta.com"]
	start_urls = (
		'http://www.loksatta.com/desh-videsh/',
	)

	def parse(self, response):
		ulink = response.xpath('//html/body/section/article/div[3]/div/h2/a/@href')
		for href in ulink:
			uRl = response.urljoin(href.extract())
			yield scrapy.Request(uRl, callback=self.parse_products, meta={'url':href.extract()})
		yield self.create_ajax_request(self.next_page)


	def create_ajax_request(self, page_number):
		ajax_template = 'http://www.loksatta.com/desh-videsh/page/{pagenum}'
		url = ajax_template.format(pagenum=page_number)
		return Request(url, callback=self.parse)

	def parse_products(self, response):
		hxs = HtmlXPathSelector(response)
		items = []
		item = BitnewsscrapItem2()
		item['title'] = hxs.select('//*[@id="headline"]/text()').extract()
		item['description'] = hxs.select('//*[@id="rightsec"]/p/text()').extract()
		item['link'] = response.meta["url"]
		item['image'] = hxs.select('//*[@id="imgholder"]/img/@*[1]').extract()
		item['pubdate'] = hxs.select('//*[@class="date"]/p/span/@*[2]').extract()
		items.append(item)
		return items
