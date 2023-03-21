import scrapy



class AppSpider(scrapy.Spider):
    name = "app"
    #allowed_domains = ["tr.wikipedia.org"]
    start_urls = ['https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi']

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable']/tbody/tr") #tr.wikipedia
       
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
                "region" :region, #('\s+', ' ', description.strip()) | content = re.sub(r"^\s+|\s+$|\n", "",cont)
                "city" : city,
                "population" : population
            }

    
