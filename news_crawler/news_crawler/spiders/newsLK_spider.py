import scrapy


class NewsLKSpider(scrapy.Spider):
    name = "news_lk"
    start_urls = [
        'https://www.news.lk/'
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
