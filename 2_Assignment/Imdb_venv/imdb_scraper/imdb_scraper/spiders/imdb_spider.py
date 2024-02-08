import scrapy


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    global start_urls
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        yield scrapy.Request(url="https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers=headers, callback=self.parse)

    def parse(self, response):
        movies = response.css('.sc-be6f1408-0')
        for movie in movies:
            print('movie_title: %s' % movie.css('h3 ::text').get())
            yield {
                'movie_title' : movie.css('h3 ::text').get(),
                'year' : movie.css('span ::text').get(),
                'rating' : movie.css('.ipc-rating-star ::text').get()
            }
            



