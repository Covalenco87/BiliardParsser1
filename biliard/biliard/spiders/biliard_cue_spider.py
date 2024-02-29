import scrapy

class BiliardScrapeSpider(scrapy.Spider):
    name = 'biliard_cue'
    start_urls = [
        'https://cue.ru/aksessuary-dlya-bilyarda/kii/',
    ]

    def parse(self, response):
        for link in response.css('div.product-name > a::attr(href)'):
            yield response.follow(link, callback=self.parse_biliard)

        for i in range(1, 14):
            next_page = f'https://cue.ru/aksessuary-dlya-bilyarda/kii/?page={i}/'
            yield response.follow(next_page, callback=self.parse)

    def parse_biliard(self, response):
        name = response.css('#tab-specification > div > div > span.attr-name > span::text').getall()
        value = response.css('#tab-specification > div > div > span.attr-text > span::text').getall()
        data = dict(zip(name, value))
        length = data.get('Длина')
        weight = data.get('Вес нетто')

        yield {
            'name': response.xpath('//*[@id="content"]/h1/text()').get(),
            'fix-price(RUB)': response.css('#product > div.price > span::text').get(),
            'disc-price(RUB)': response.css('#product > div.price > span.price-new > span::text').get(),
            'length(cm)': length,
            'weight(g)': weight,
            'image': response.css('#zoom1::attr(href)').get(),
            'link': response.xpath('/html/head/link[1]/@href').get(),
        }
