
products = response.css('div.product-item-info')
price =  products.css('span.price:text').get().replace("£","")
name = products.css('a.product-item-link::text').get()
link = products.css('a.product-item-link').attrib['href']