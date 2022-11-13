# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RottenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    creators = scrapy.Field()
    ratings = scrapy.Field()
    description = scrapy.Field()
    starring = scrapy.Field()
    network = scrapy.Field()
    genre = scrapy.Field()
    premiere = scrapy.Field()
    producer = scrapy.Field()
