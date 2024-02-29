
import scrapy
import pandas as pd

class BiliardScrapeSpider(scrapy.Spider):
    name = 'biliard'
    start_urls = [
        'https://www.luza.ru/catalog/piramida_cues/',
    ]

    def parse(self, response):
        for link in response.css('div.desc_name a::attr(href)'):
            yield response.follow(link, callback=self.parse_biliard)

        for i in range(1, 90):
            next_page = f'https://www.luza.ru/catalog/piramida_cues/?PAGEN_1={i}/'
            yield response.follow(next_page, callback=self.parse)
         
    def parse_biliard(self, response):
        yield {
            'name': response.xpath('//*[@id="pagetitle"]/text()').get(),
            'price(RUB)': response.css('div.cost.prices.clearfix > div > div:nth-child(1) > span > span.price_value::text').get(),
            'length(cm)': response.css('table.props_list > tr:nth-child(2) > td.char_value > span::text').get().strip(),
            'weight(g)': response.css('table.props_list > tr:nth-child(3) > td.char_value > span::text').get().strip(),
            'balance(cm)': response.css('table.props_list > tr:nth-child(4) > td.char_value > span::text').get().strip(),
            'image': response.urljoin(response.css('div.item_slider > div.slides a').attrib['href']),
            'link': response.xpath('/html/head/link[4]/@href').get(),
        }

