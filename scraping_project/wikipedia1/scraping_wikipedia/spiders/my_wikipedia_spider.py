import scrapy
from ..items import ScrapingWikipediaItem

class ScrapingWikipedia(scrapy.Spider):
    name = 'my_wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_companies_of_Italy']
    # name and start_url are expected by scrapy.Spider and should not be changed

    def parse(self, response):

        
        items = ScrapingWikipediaItem()
        
        ## the table we want is the second in the whole page
        ## the table contains tr elements - table rows
        table = response.xpath("//table[2]").css("tr")
        
        
        ## we filter out the first row that contains the header
        for row in table[1:]: 
            ## we iterate over the rows, and pick the elements we want,
            ## we put them in a list, and send them to the database
            list_to_insert = []

            ## the name
            list_to_insert.append(row.xpath("td[1]//text()").get() )

            ## the wiki url
            list_to_insert.append( "https://en.wikipedia.org" + \
                row.xpath("td[1]/a/@href").get() )

            ## the industry
            list_to_insert.append(row.xpath("td[2]/text()").get().strip("\n") )

            ## the sector
            list_to_insert.append(row.xpath("td[3]/text()").get().strip("\n") )

            ## the headquarters
            list_to_insert.append(row.xpath("td[4]/a/text()").get().strip("\n") )            

            ## founded in
            list_to_insert.append(row.xpath("td[5]/text()").get().strip("\n") ) 
            
            
            items['row'] = list_to_insert
            
            yield items
            
            
