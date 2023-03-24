import scrapy
import pymongo

class AppSpider(scrapy.Spider):
    name = "app"
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


'''class AppSpider(scrapy.Spider):
    name = "app"
    #allowed_domains = ["tr.wikipedia.org"]
    start_urls = ['https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi']

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable']/tbody/tr")[2:] #tr.wikipedia
       
        for result in results:
            #scraping region from the website
            region = result.xpath(".//td[7]/a/text()").get()
            city = result.xpath(".//td[2]/a/text()").get()
            population = result.xpath(".//td[6]/text()").get()
            if region == None:
                region= result.xpath(".//td[7]/text()").get()
                
            
            
           
            #making a yield
            yield{
                "country" : "Netherland",
                "region" :region.replace('\n',''),
                "city" : city,
                "population" : population
            }'''

    
            
