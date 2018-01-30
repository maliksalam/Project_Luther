import scrapy

# define url_list

url_list = ['https://www.the-numbers.com/movie/budgets/all/' + str(i) for i in range(101,5402,100)] #final end point is 5402
url_list = ['https://www.the-numbers.com/movie/budgets/all'] + url_list

class MovieSpider(scrapy.Spider):
    name = 'thenumbers'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = url_list


    def parse(self, response):

            release_dates = (response.xpath('//div[@id="page_filling_chart"]/center/table/tr/td/a/text()').extract())

            titles = (response.xpath('//div[@id="page_filling_chart"]/center/table/tr/td/b/a/text()').extract())

            budgets = (response.xpath('//div[@id="page_filling_chart"]/center/table/tr/td[4]/text()').extract())

            dom_gross = (response.xpath('//div[@id="page_filling_chart"]/center/table/tr/td[5]/text()').extract())

            ww_gross = (response.xpath('//div[@id="page_filling_chart"]/center/table/tr/td[6]/text()').extract())

            for i in range(len(titles)):
                yield {
                    'title': titles[i],
                    'release_date': release_dates[i],
                    'budget': budgets[i],
                    'dom_gross': dom_gross[i],
                    'ww_gross': ww_gross[i],
                }
