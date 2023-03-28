import scrapy
import pymongo


class AmericaSpider(scrapy.Spider):
    name = "america"
    start_urls = ["https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"]

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["america"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable'][1]/tbody/tr")[1:]
       
        for result in results:
            #scraping region from the website
            city = result.xpath(".//td[1]/i/a/text() | .//td[1]/i/b/a/text() | .//td[1]/b/a/text() | .//td[1]/a/text() | .//td[1]/b/a/i/text()").get()
            region = result.xpath(".//td[2]/a/text()").get()
            population = result.xpath(".//td[3]/text()").get()
            
            #inserting data to MongoDB
            item = {
                "country" : "USA",
                "region" :region.strip(),
                "city" : city.strip(),
                "population" : population.replace('\n','').strip()
            }
            try:
                self.collection.insert_one(item)
                yield item
            except pymongo.errors.WriteError as e:
                print("Kaydetme hatası:", e)
                
            #making a yield
            yield item
    
    
    
    '''class AmericaSpider(scrapy.Spider):
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
                "region" :region,
                "city" : city,
                "population" : population.replace('\n','')
            }'''
