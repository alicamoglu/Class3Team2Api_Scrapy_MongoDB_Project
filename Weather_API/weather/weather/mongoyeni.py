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
        results = response.xpath("//table[@class='wikitable sortable'][1]/tbody/tr")[2:]
       
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


class GermanySpider(scrapy.Spider):
    name = "germany"
    start_urls = ["https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"]

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["germany"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable zebra'][2]/tbody/tr")[2:]
       
        for result in results:
            #scraping region from the website
            city = result.xpath(".//td[2]/a/text()").get()
            region = result.xpath(".//td[9]/text()").get()
            population = result.xpath(".//td[8]/text()").get()  
            
            #inserting data to MongoDB
            item = {
                "country" : "Germany",
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


class NetherlandSpider(scrapy.Spider):
    name = "netherland"
    start_urls = ["https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi"]

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["netherland"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable']/tbody/tr")[2:]
       
        for result in results:
            #scraping region from the website
            region = result.xpath(".//td[7]/a/text()").get()
            city = result.xpath(".//td[2]/a/text()").get()
            population = result.xpath(".//td[6]/text()").get()
            if region == None:
                region= result.xpath(".//td[7]/text()").get() 
            
            
            #inserting data to MongoDB
            item = {
                "country" : "Netherland",
                "region" :region.replace('\n',''),
                "city" : city,
                "population" : population
            }
            try:
                self.collection.insert_one(item)
                yield item
            except pymongo.errors.WriteError as e:
                print("Kaydetme hatası:", e)
                
            yield item    

        self.collection.insert_one(item)
                 