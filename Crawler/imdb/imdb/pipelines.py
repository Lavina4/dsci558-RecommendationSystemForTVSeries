# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from imdb.items import TVSeriesItem
import json

class ImdbPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(item, TVSeriesItem):
            adapter['title'] = adapter['title']
            adapter['imdb_rating'] = float(adapter['imdb_rating'][0]) if adapter['imdb_rating'][0] != 'NA' else 'NA'
            adapter['plot'] = adapter['plot'][0].strip()
            adapter['genre'] = adapter['genre']
            adapter['creators'] = adapter['creators']
            adapter['stars'] = adapter['stars']
            adapter['top_cast'] = adapter['top_cast']
            adapter['num_seasons'] = int(adapter['num_seasons'][0].split(' ')[0]) if adapter['num_seasons'][0] != 'NA' else 'NA'
            adapter['release_date'] = adapter['release_date']
            adapter['language'] = adapter['language']
            adapter['country_of_origin'] = adapter['country_of_origin']
            adapter['production_company'] = adapter['production_company']
        return item

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.imdb_file = open('imdb_tvseries.jsonl', 'w')

    def close_spider(self, spider):
        self.imdb_file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.imdb_file.write(line)
        return item