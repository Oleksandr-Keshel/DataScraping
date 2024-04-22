import scrapy
from ..items import SmartphoneItem, ShopItem


class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.ua"]
    start_urls = [
        f"https://hotline.ua/ua/mobile/mobilnye-telefony-i-smartfony/?p={page}" for page in range(1, 5)
    ]

    def parse(self, response):
        items = response.css('div.list-body__content').css('.list-item')
        for item in items:
            name = item.css('.list-item__title-container a').css('::text').get()
            url = f"https://hotline.ua/{item.css('.list-item__title-container a').xpath('@href').get()}"
            image_url = f"https://hotline.ua/{item.css('a.list-item__img img').xpath('@src').get()}"
            yield SmartphoneItem(
                name=name,
                url=url,
                image_urls=[image_url]
            )
            yield scrapy.Request(
                url=url,
                callback=self.parse_shop,
                meta={
                    "smartphone_name": name
                }
            )

    def parse_shop(self, response):
        items = response.css('div.list').css('.list__item')
        for item in items:
            name = item.css('.shop__header a').css('::text').get()
            url = f"https://hotline.ua/{item.css('.shop__header a').xpath('@href').get()}"
            image_url = f"https://hotline.ua/{item.css('a.shop__logo img').xpath('@src').get()}"
            price = item.css('span.price__value ::text').get()
            smartphone_name = response.meta.get("smartphone_name")
            yield ShopItem(
                name=name,
                url=url,
                image_urls=[image_url],
                price=price,
                smartphone_name=smartphone_name
            )