import scrapy

# define url_list

url_list = ['http://www.boxofficemojo.com/oscar/chart/?view=allmovies&yr={}&p=.htm'.format(i) for i in range(1980,2018)] #range is 1980 - 2017

class MovieSpider(scrapy.Spider):
    name = 'oscars'

    custom_settings = {
        "HTTPCACHE_ENABLED": True
    }

    start_urls = url_list


    def parse(self, response):

            titles = response.xpath('//div[@id="body"]/table//table/tr/td//font/a//b/text()').extract()
            oscar_noms_list = response.xpath('//div[@id="body"]/table//table/tr/td/font/text()').extract()[5::6]
            oscars_list = response.xpath('//div[@id="body"]/table//table/tr/td/font/text()').extract()[6::6]

            for i in range(len(titles)):
                yield {
                    'title': titles[i],
                    'oscar_noms': oscar_noms_list[i],
                    'oscars': oscars_list[i],
                }
