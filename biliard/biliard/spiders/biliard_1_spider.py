import scrapy

class BiliardScrapeSpider(scrapy.Spider):
    name = 'biliard1'
    start_urls = [
        'https://www.billiard1.ru/catalog/kii/',
    ]

    def parse(self, response):
        for link in response.css('div.item-title > a::attr(href)'):
            yield response.follow(link, callback=self.parse_biliard)

        for i in range(1, 48):
            next_page = f'https://www.billiard1.ru/catalog/kii/?PAGEN_1={i}/'
            yield response.follow(next_page, callback=self.parse)

    def parse_biliard(self, response):

        name = response.css('table:nth-child(1) > tbody > tr > td.char_name > div > span::text').getall()
        value = response.css('table:nth-child(1) > tbody > tr > td.char_value > span::text').getall()
        data = dict(zip(name, value))
        length = data.get('Длина кия')
        weight = data.get('Вес кия')

        if length == None:
            clear_length = 0
        elif len(length) > 10:
            clear_length = length.strip()
        else:
            clear_length = length

        if weight == None:
            clear_weight = 0
        elif len(weight) > 10:
            clear_weight = weight.strip()
        else:
            clear_weight = weight
        yield {
            'name': response.xpath('//*[@id="pagetitle"]/text()').get(),
            'price(RUB)': response.css('div.with_matrix.price_matrix_wrapper > div > div > div > span.price_value::text').get(),
            'length(cm)': clear_length,
            'weight(g)': clear_weight,
            'image': response.urljoin(response.css('div.product-detail-gallery.swipeignore.js-notice-block__image > div > link').attrib['href']) ,
            'link': response.urljoin(response.css('div.right-icons.wb.header__top-item > div.auth_wr_inner a::attr(data-param-backurl)')),
        }