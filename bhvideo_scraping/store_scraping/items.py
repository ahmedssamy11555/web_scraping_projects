# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field
import scrapy


class StoreScrapingItem(scrapy.Item):
    
    product_name =scrapy.Field()
    product_price =scrapy.Field()
    key_feats =scrapy.Field()
    image_link =scrapy.Field()
    internal_link =scrapy.Field()
    availability  =scrapy.Field()
    
    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
         
        
     
        
    
    
    
    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
