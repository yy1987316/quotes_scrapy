# -*- coding: utf-8 -*-
import scrapy
from quotes.items import QuotesItem

class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            q_item = QuotesItem()
            q_item['text'] = quote.css('.text::text').extract_first()
            q_item['author'] = quote.css('.author::text').extract_first()
            q_item['tags'] = quote.css('.tags .tag::text').extract()
            yield q_item

        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)