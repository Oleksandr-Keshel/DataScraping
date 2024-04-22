# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy





class SmartphoneItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()

class ShopItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    price = scrapy.Field()
    smartphone_name = scrapy.Field()
