import scrapy
from rotten.items import RottenItem

class rotten(scrapy.Spider):
    name = "rotten"
    url = ['https://www.rottentomatoes.com/browse/tv_series_browse/genres:action,adventure,animation,anime,biography,comedy,crime,documentary,drama,entertainment,faith_and_spirituality,fantasy,game_show,health_and_wellness,history,holiday,horror,house_and_garden,kids_and_family,lgbtq,music,musical,mystery_and_thriller,nature,news,reality,romance,sci_fi,short,soap,special_interest,sports,stand_up,talk_show,travel,variety,war,western~sort:popular?page=10']
    start_urls = url

    def parse(self, response):
        ls = []
        item = RottenItem()
        for i in response.xpath('//div[@class ="discovery-tiles__wrap"]/a[@class = "js-tile-link"]'):
            #item = i #i.xpath('[@class= "js-tile-link"]/tile-dynamic/div/span/text()')
            #item['title'] = i.xpath('tile-dynamic/div/span/text()').get().strip()
            #print(item.strip())
            ls.append("https://www.rottentomatoes.com" + i.xpath('@href').get())
            #yield item
            #ls.append(item)
        #print(ls)
        for i in ls:
            yield scrapy.Request(i, self.parse_movies)


    def parse_movies(self, response):
        #print("Hello from parse_movies")
        #item = MoviesItem()
        item = RottenItem()
        ls = []
        #print(response.)
        #item['filename'] = 'Kshitij Ahuja2.json'
        item['title'] = response.xpath('//*[@data-type = "title"]/text()').get().strip()
        item['creators'] = response.xpath('//*[@data-qa = "series-info-creators"]/../a/text()').getall()
        rating = response.xpath('//span[@class = "mop-ratings-wrap__percentage"]/text()').getall()
        rating = [s.strip() for s in rating]
        item['ratings'] = rating
        item['description'] = response.xpath('//*[@id = "movieSynopsis"]/text()').get()
        item['starring'] = response.xpath('//*[@data-qa = "series-info-cast"]/../a/text()').getall()
        item['network'] = response.xpath('//*[@data-qa = "series-details-network"]/text()').get()
        item['genre'] = response.xpath('//*[@data-qa = "series-details-genre"]/text()').getall()
        item['premiere'] = response.xpath('//*[@data-qa = "series-details-premiere-date"]/text()').get()
        item['producer'] = response.xpath('//*[@data-qa = "series-details-producer"]/text()').getall()

        yield item
        #ls.apend(item['creators'])
        #print(ls)