# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TopCast(scrapy.Item):
    name = scrapy.Field()
    character_played = scrapy.Field()

class TVSeriesItem(scrapy.Item):
    title = scrapy.Field()
    imdb_rating = scrapy.Field()
    plot = scrapy.Field()
    genre = scrapy.Field()
    creators = scrapy.Field()
    stars = scrapy.Field()
    top_cast = scrapy.Field()
    num_seasons = scrapy.Field()
    release_date = scrapy.Field()
    language = scrapy.Field()
    country_of_origin = scrapy.Field()
    production_company = scrapy.Field()
