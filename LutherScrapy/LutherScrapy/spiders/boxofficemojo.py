import scrapy

# define url_list
url_list= ['http://www.boxofficemojo.com/movies/alphabetical.htm']

for i in range(65,91): #range(65,91)
    for j in range(1,14): # range(1,14)
        url_list.append('http://www.boxofficemojo.com/movies/alphabetical.htm?letter={}&page={}&p=.htm'.format(chr(i),j))

class MovieSpider(scrapy.Spider):
    name = 'boxofficemojo'

    custom_settings = {
        "HTTPCACHE_ENABLED": True
    }

    start_urls = url_list


    def parse(self, response):
        # Extract the links to the individual alpha pages
        partial_links = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td/font/a/b/../@href').extract()
        movie_links = ['http://www.boxofficemojo.com' + link for link in partial_links]
        titles = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td/font/a/b/text()').extract()
        dom_grosses = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td[3]/font/text()').extract()[1:]
        widest_releases = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td[4]/font/text()').extract()[1:]
        opening_we_grosses = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td[5]/font/text()').extract()[1:]
        opening_releases = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td[6]/font/text()').extract()
        release_dates = response.xpath('//div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td[7]/font/text() | //div[@id="body"]/div/table/tr/td/table/tr/td/table/tr/td/font/a/text()').extract()

        for i in range(len(movie_links)):
            yield scrapy.Request(
                url = movie_links[i],
                callback = self.parse_movie,
                meta = {'title': titles[i],
                        'dom_gross': dom_grosses[i],
                        'widest_release': widest_releases[i],
                        'opening_we_gross': opening_we_grosses[i],
                        'opening_release': opening_releases[i],
                        'release_date': release_dates[i],
                        'url': movie_links[i]
                        }
            )

    def parse_movie(self, response):

            title = response.request.meta['title']

            release_date = response.request.meta['release_date']

            dom_gross = response.request.meta['dom_gross']

            widest_release = response.request.meta['widest_release']

            opening_we_gross = response.request.meta['opening_we_gross']

            opening_release = response.request.meta['opening_release']

            url = response.request.meta['url']

            studio = response.xpath('//div[@id="body"]/table/tr[2]/table/tr/td/table[1]/tr/td[2]/table/tr/td/center/table/tr/td/b/a/text()').extract()[0]

            genre = response.xpath('//div[@id="body"]/table/tr[2]/table/tr/td/table[1]/tr/td[2]/table/tr/td/center/table/tr/td/b/text()').extract()[0]

            runtime = response.xpath('//div[@id="body"]/table/tr[2]/table/tr/td/table[1]/tr/td[2]/table/tr/td/center/table/tr/td/b/text()').extract()[1]

            mpaa_rating = response.xpath('//div[@id="body"]/table/tr[2]/table/tr/td/table[1]/tr/td[2]/table/tr/td/center/table/tr/td/b/text()').extract()[2]

            budget = response.xpath('//div[@id="body"]/table/tr[2]/table/tr/td/table[1]/tr/td[2]/table/tr/td/center/table/tr/td/b/text()').extract()[3]

            ww_gross = response.xpath('//b[contains(text(), "Worldwide")]/../following-sibling::td/b/text()').extract_first()

            try:
                directors = response.xpath('//a[contains(text(), "Director")]/../../following-sibling::td//text()').extract()
            except:
                directors = None

            try:
                writers = response.xpath('//a[contains(text(), "Writer")]/../../following-sibling::td//text()').extract()
            except:
                writer = None

            try:
                producers = response.xpath('//a[contains(text(), "Producer")]/../../following-sibling::td//text()').extract()
            except:
                producers = None

            try:
                actors = response.xpath('//a[contains(text(), "Actor")]/../../following-sibling::td//text()').extract()
            except:
                actors = None

            try:
                theatrical_run = response.xpath('//td[contains(text(), "In Release")]/following-sibling::td/text()').extract_first().strip()
            except:
                theatrical_run = None

            yield {
                'title': title,
                'release_date': release_date,
                'budget' : budget,
                'dom_gross': dom_gross,
                'ww_gross': ww_gross,
                'widest_release': widest_release,
                'opening_we_gross': opening_we_gross,
                'opening_release': opening_release,
                'theatrical_run': theatrical_run,
                'url': url,
                'studio': studio,
                'genre': genre,
                'runtime': runtime,
                'mpaa_rating': mpaa_rating,
                'directors': directors,
                'writers': writers,
                'producers': producers,
                'actors': actors,
            }
