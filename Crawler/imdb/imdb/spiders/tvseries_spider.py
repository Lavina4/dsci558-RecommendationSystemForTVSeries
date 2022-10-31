import scrapy
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
from imdb.items import TVSeriesItem, TopCast
import logging
from scrapy.utils.log import configure_logging

class TVSeriesSpider(scrapy.Spider):
    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.ERROR
    # )
    name = "tvseries"
    start_urls = [
        "https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=comedy,romance&explore=title_type,genres&title_type=tvSeries",
        "https://www.imdb.com/search/title/?genres=action,comedy&explore=title_type,genres&title_type=tvSeries",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tvseries_table = soup.select_one('div[class="lister-list"]')
        tvseries = tvseries_table.select('div[class="lister-item mode-advanced"]')
        for series in tvseries:
            yield response.follow(response.urljoin(series.find('h3', class_='lister-item-header').a['href']), callback=self.tvseries_parse)

        next_selector = soup.select_one('div[id="main"] > div[class="article"] > div[class="desc"] a[class="lister-page-next next-page"]')
        if next_selector:
            yield response.follow(response.urljoin(next_selector['href']), callback=self.parse)

    def tvseries_parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        if soup.select_one('div[data-testid="hero-subnav-bar-left-block"] > a') and ('in development' not in soup.select_one('div[data-testid="hero-subnav-bar-left-block"] > a').text.lower()):
            title = soup.select_one('div h1[data-testid="hero-title-block__title"]').text
            tvseries_stars_creators = soup.select('div[data-testid="title-pc-wide-screen"] > ul[class="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt"] > li')
            plot_selector = soup.select_one('div[data-testid="plot"] > span[data-testid="plot-xl"]')
            plot = soup.select_one('div[data-testid="plot"] > span[data-testid="plot-xl"]').get_text(strip=True) if plot_selector else 'NA'

            creators_info = None
            for creators_list in tvseries_stars_creators:
                if (creators_list.find('span') and creators_list.find('span').text in ['Creator', 'Creators']) or (creators_list.find('a')  and creators_list.find('a').text in ['Creator', 'Creators']):
                    creators_info = creators_list.find_all('li')
                    break
            creators = [creator.a.string for creator in creators_info] if creators_info else ['']

            stars_info = None
            for stars_list in tvseries_stars_creators:
                if stars_list.find('a').text in ['Star', 'Stars']:
                    stars_info = stars_list.find_all('li')
                    break
            stars = [star.a.string for star in stars_info] if stars_info else ''

            num_seasons = 'NA'
            num_seasons_selector = soup.select_one('div[data-testid="episodes-browse-episodes"] label[for="browse-episodes-season"]')
            if num_seasons_selector:
                num_seasons = num_seasons_selector.text
            elif soup.select('div[data-testid="episodes-browse-episodes"] > div a div'):
                for s in soup.select('div[data-testid="episodes-browse-episodes"] > div a div'):
                    if 'season' in s.text.lower():
                        num_seasons = s.text

            topcast_div = soup.select('section[data-testid="title-cast"] div[data-testid="title-cast-item"] > div:not(div[data-testid="title-cast-item__avatar"])')
            casts_info = []
            if topcast_div:
                for cast in topcast_div:
                    if cast and cast.find('a'):
                        name = cast.find('a').text
                        character = cast.select_one('div[class="title-cast-item__characters-list"]').find('span').text if cast.select_one('div[class="title-cast-item__characters-list"]') else ''
                        casts_info.append(TopCast(name = name, character_played = character))
            casts_info = casts_info if len(casts_info) > 0 else 'NA'

            rating_info = soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating__score"]')
            rating = rating_info.find('span').text if rating_info else 'NA'

            tvseries_genre_selector = soup.select('div[data-testid="genres"] a')
            tvseries_genres = []
            for tvseries_genre in tvseries_genre_selector:
                tvseries_genres.append(tvseries_genre.text)
            tvseries_genres = tvseries_genres if len(tvseries_genres) > 0 else 'NA'

            tvseries_info = soup.select_one('div[data-testid="title-details-section"] > ul')
            release_date_selector = tvseries_info.select('li[data-testid="title-details-releasedate"] ul > li')
            release_date = []
            for rd in release_date_selector:
                release_date.append(rd.find('a', recursive=False).text)
            release_date = release_date if len(release_date) > 0 else 'NA'

            country_of_origin_selector = tvseries_info.select('li[data-testid="title-details-origin"] ul > li')
            country_of_origin = []
            for cor in country_of_origin_selector:
                country_of_origin.append(cor.find('a', recursive=False).text)
            country_of_origin = country_of_origin if len(country_of_origin) > 0 else 'NA'

            language_selector = tvseries_info.select('li[data-testid="title-details-languages"] ul > li')
            tvseries_language = []
            for language in language_selector:
                tvseries_language.append(language.find('a', recursive=False).text)
            tvseries_language = tvseries_language if len(tvseries_language) > 0 else 'NA'

            production_company_selector = tvseries_info.select('li[data-testid="title-details-companies"] ul > li')
            production_company = []
            for pc in production_company_selector:
                production_company.append(pc.find('a').text)
            production_company = production_company if len(production_company) > 0 else ''

            item = ItemLoader(TVSeriesItem(), response)
            item.add_value('title',  title)
            item.add_value('imdb_rating',  rating)
            item.add_value('plot', plot)
            item.add_value('genre', tvseries_genres)
            item.add_value('creators', creators)
            item.add_value('stars', stars)
            item.add_value('top_cast', casts_info)
            item.add_value('num_seasons', num_seasons)
            item.add_value('release_date', release_date)
            item.add_value('language', tvseries_language)
            item.add_value('country_of_origin', country_of_origin)
            item.add_value('production_company', production_company)

            yield item.load_item()