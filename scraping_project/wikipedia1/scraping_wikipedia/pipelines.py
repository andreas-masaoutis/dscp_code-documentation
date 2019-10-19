# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tinydb import TinyDB

class ScrapingWikipediaPipeline(object):
    
    ## when this class is used (new instance), certain actions take place
    def __init__(self):
        ## the basic thing to do is to create a connection to the database
        self.create_connection()

        
    def create_connection(self):
        ## connect to database, or create database if it does not exist
        ## the extra parameters-sort_keys etc,just beuatify the json file
        self.db = TinyDB('../wikipedia1_db.json', sort_keys=True, 
            indent=4, separators=(',', ': '))
        ## This will delete all documents. Use to ensure new connections
        ## start with a clean database.
        self.db.purge()    

    
    def store_db(self, item):
        ## the spider sends the parsed item
        ## which is then inserted in the database
        self.db.insert( 
        {'row' : item['row']} )

    
    def process_item(self, item, spider):
        ## the actual insertion into the database takes place here
        self.store_db(item)
        return item
