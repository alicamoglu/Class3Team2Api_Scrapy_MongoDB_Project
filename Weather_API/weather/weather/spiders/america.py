import scrapy


class AmericaSpider(scrapy.Spider):
    name = "america"
    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"]

    def parse(self, response):
     
        results = response.xpath("//table[@class='wikitable sortable'][1]/tbody/tr")[2:] #en.wikipedia
       
        for result in results:
            #scraping region from the website
                
            city = result.xpath(".//td[1]/i/a/text()").get() #//table[@class="wikitable sortable"]/tbody/tr/td/i/a/text()
            region = result.xpath(".//td[2]/a/text()").get()
            population = result.xpath(".//td[3]/text()").get()
            
            if city == None:
                city= result.xpath(".//td[1]/i/b/a/text()").get()
                if city == None :
                    city = result.xpath(".//td[1]/b/a/text()").get()
                    if city == None:
                        city = result.xpath(".//td[1]/a/text()").get()
                        if city == None:
                            city = result.xpath(".//td[1]/b/a/i/text()").get()
                        
        #making a yield
            yield{
                "country" : "USA",
                "region" :region, #('\s+', ' ', description.strip()) | content = re.sub(r"^\s+|\s+$|\n", "",cont)
                "city" : city,
                "population" : population.replace('\n','')
            }
