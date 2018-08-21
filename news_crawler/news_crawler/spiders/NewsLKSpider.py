import scrapy


class NewsLKSpider(scrapy.Spider):
    name = "news_lk"
    news_id = 0

    # Url
    #   Latest News,
    #   President - Parliament - Prime Minister,
    #   political-current-affairs
    #   https://www.news.lk/cabinet-decusions
    #   sports-travel

    start_urls = [
        'https://www.news.lk/news/sri-lanka',
        'https://www.news.lk/news/politics',
        'https://www.news.lk/news/political-current-affairs',
        'https://www.news.lk/cabinet-decusions',
        'https://www.news.lk/news/sports-travel'
    ]

    def parse(self, response):
        news_blocks = response.css("div.itemContainerLast")
        for news_block in news_blocks:
            self.news_id = self.news_id + 1
            date = news_block.css("span.yj_date::text").extract_first().decode().replace('\r\n      ', '')
            month = news_block.css("span.yj_date span::text").extract_first()
            title = news_block.css("h3.catItemTitle a::text").extract_first()
            source = response.url.split("/")[-1].partition("?")[0]

            yield {
                'id': self.news_id,
                'date': date,
                'month': month,
                'title': title,
                'source': source
            }

        next_page = response.css('.pagination-next a::attr(href)').extract_first()
        page_number = int(next_page.split("=")[-1]) / 10
        if next_page is not None and page_number < 15:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
