import scrapy
from ..items import ScrapingWikipediaItem
from tinydb import TinyDB

class ScrapingWikipedia(scrapy.Spider):
    
    def create_url_list():
        ## we search the database of italian companies we set up previously,
        ## for their wikipedia urls, to be used by this spider
        
        ## create connection to previously established database
        db = TinyDB('../wikipedia1_db.json', sort_keys=True, 
            indent=4, separators=(',', ': '))
        ## TinyDB allows us to iterate over its content-documents
        url_list = []
        for doc in db:
            ## doc['row'] is a list. At position 2 we find the url
            url_list.append(doc['row'][1]) 

        return url_list
        
    
    
    name = 'my_wikipedia'
    start_urls = create_url_list()
    # name and start_url are expected by scrapy.Spider and should not be changed

    def parse(self, response):

        
        items = ScrapingWikipediaItem()
        
        ## we get out a list of all the text pieces of the text paragraphs
        text_pieces_list = response.xpath('//p//text()').getall()
        
        final_text = ""
        
        for text_piece in text_pieces_list: 
            
            final_text += text_piece.replace("\n", " ")
            
        ## we also return the url, so that we can later use it as a key
        ## to connect the documents in the two databases   
        items['complete_text'] = [response.url, final_text]
            
        yield items

