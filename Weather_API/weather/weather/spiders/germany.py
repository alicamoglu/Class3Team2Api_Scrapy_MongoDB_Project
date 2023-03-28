import scrapy
import pymongo

class GermanySpider(scrapy.Spider):
    name = "germany"
    start_urls = ["https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"]

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["germany"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable zebra'][2]/tbody/tr")[1:]
       
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


'''class GermanySpider(scrapy.Spider):
    name = "germany"
    #allowed_domains = ["de.wikipedia.org"]
    start_urls = ["https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable zebra'][2]/tbody/tr")[2:] #en.wikipedia
       
        for result in results:
            #scraping region from the website 
            city = result.xpath(".//td[2]/a/text()").get()
            region = result.xpath(".//td[9]/text()").get()
            population = result.xpath(".//td[8]/text()").get()                       
                            
            #making a yield
            yield{
                "country" : 'Germany',
                "region" :region.replace('\n',''), 
                "city" : city,
                "population":population
                }'''
    
