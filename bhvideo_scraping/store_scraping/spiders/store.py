
import scrapy

class StoreSpider(scrapy.Spider):
    name = 'store'
    #Request all the categories pages
    
    
    def response_is_ban(self, request, response):
        return b'banned' in response.body

    def exception_is_ban(self, request, exception):
        return None
    
    
    def start_requests(self):
        urls = ['https://www.bhphotovideo.com/c/browse/Photography/ci/989/N/4294538916',
 'https://www.bhphotovideo.com/c/browse/Computers-Solutions/ci/9581/N/4294542559',
 'https://www.bhphotovideo.com/c/browse/Professional-Video/ci/3755/N/4294545851',
 'https://www.bhphotovideo.com/c/browse/Lighting-Studio/ci/1161/N/4294551176',
 'https://www.bhphotovideo.com/c/browse/Professional-Audio/ci/12154/N/4294550705',
 'https://www.bhphotovideo.com/c/browse/Mobile/ci/8565/N/4294542748',
 'https://www.bhphotovideo.com/c/browse/Home-Entertainment/ci/4600/N/4294544179',
 'https://www.bhphotovideo.com/c/browse/Camcorders/ci/1820/N/4294548420',
 'https://www.bhphotovideo.com/c/browse/Surveillance-Video/ci/3496/N/4293342959',
 'https://www.bhphotovideo.com/c/browse/Binoculars-Scopes/ci/978/N/4294541872',
 'https://www.bhphotovideo.com/c/browse/A-V-Presentation/ci/3644/N/4294546288',
 'https://www.bhphotovideo.com/c/browse/more/ci/47088',
 'https://www.bhphotovideo.com/c/category/2870/Used_Equipment.html',
 'https://www.bhphotovideo.com/c/buy/rebates-promotions/ci/22144/N/4019732813']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.categories) 
            
            
    #list all the links of the categories and give them to the parse function         
    def categories(self,response):
        categories_urls = response.xpath('//section[@data-selenium="categorySection"]//div[@data-selenium="categoryGroupGridCategory"]/a/@href').extract()
        for category_url in categories_urls:
            yield response.follow(url = category_url,callback=self.parse)    

    def parse(self, response):
        # Parse and extract details for each item
        for item in response.xpath('//div[@data-selenium="miniProductPage"]'):
            product_name  = item.xpath('.//span[@data-selenium="miniProductPageProductName"]/text()').get()
            product_price = item.xpath('.//span[@data-selenium="uppedDecimalPriceFirst"]/text()').get()
            key_feats     = item.xpath('.//*[@data-selenium="miniProductPageSellingPointsListItem"]/text()').getall()
            image_link    = item.xpath('.//img[@data-selenium="miniProductPageImg"]/@src').get()
            internal_link = item.xpath('.//a[@data-selenium="miniProductPageProductNameLink"]/@href').extract()
            availability  = item.xpath('.//div/span[@data-selenium="stockStatus"]/text()').get()
            category = response.xpath('.//h1[@data-selenium="titleNumberingTitle"]/text()').extract_first()

            # We need to join the internal link with the base url
            # to get the complete product link
            internal_link = ''.join(map(str, internal_link)) 
            if internal_link is not None:
                product_link = response.urljoin(internal_link)
            yield {
                'Product Name': product_name,
                'Product Price': product_price,
                'Key Features': key_feats,
                'Availability': availability,
                'Image Link': image_link,
                'Product Link': product_link,
                'category':category
                }

        pagination_links = response.xpath('.//ul/li/a[@data-selenium="listingPagingLink"]/@href').getall()
        yield from response.follow_all(pagination_links, callback=self.parse)
        