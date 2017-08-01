#!/bin/bash
mkdir /home/neelesh/Desktop/new_folder

#HINDI - Dainik Bhaskar
scrapy crawl dainik

#MARATHI - Loksatta
scrapy crawl loksatta

#OneIndia - TMAIL, TELUGU, MARATHI
scrapy crawl oneindia-telugu
scrapy crawl oneindia-tamil
scrapy crawl oneindia-kannada

#ENGLISH - Times Of India
scrapy crawl toi-india
scrapy crawl toi-world
scrapy crawl toi-business
scrapy crawl toi-cricket
scrapy crawl toi-sports
scrapy crawl toi-tech
scrapy crawl toi-health
scrapy crawl toi-edu
scrapy crawl toi-entertainment
scrapy crawl toi-lifestyle

#ENGLISH - Economic Times
scrapy crawl et-industry
scrapy crawl et-tech
scrapy crawl et-markets
scrapy crawl et-economy
scrapy crawl et-smallbiz
scrapy crawl et-magazines
scrapy crawl et-wealth
scrapy crawl et-jobs