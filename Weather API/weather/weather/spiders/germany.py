import scrapy


class GermanySpider(scrapy.Spider):
    name = "germany"
    #allowed_domains = ["de.wikipedia.org"]
    start_urls = ["https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"]

    def parse(self, response):
        results = response.xpath("//table[@class='wikitable sortable zebra'][2]/tbody/tr") #en.wikipedia
       
        for result in results:
            #scraping region from the website 
            city = result.xpath(".//td[2]/a/text()").get()
            region = result.xpath(".//td[9]/text()").get()
                       
                            
            #making a yield
            yield{
                "country" : 'Germany',
                "region" :region, 
                "city" : city
                }
