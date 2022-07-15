
from selenium import webdriver
import requests
import io
from PIL import Image
import time
from selenium.webdriver.common.by import By
import csv
from datetime import datetime
import urllib.request



PATH = "C:\\Users\\Sami\Desktop\\google_images\\chromedriver.exe"

wd = webdriver.Chrome(executable_path = PATH)
 
 
def search_imag(search_word) :    
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}logo&oq={q}logo&"
    #loding the page
    return search_url.format(q=search_word)

            
def get_image_url(wd,delay,url):
    #filteration
    wd.get(url)
    filter = wd.find_element_by_xpath('//div[@class="PNyWAd ZXJQ7c"]')
    filter.click()
    time.sleep(delay)
    size = wd.find_element_by_xpath('//div[@aria-label="Size"]')
    size.click()
    large_image = wd.find_element_by_xpath('//a[@aria-label="Large"]')
    large_image.click()
    time.sleep(delay)
    color = wd.find_element_by_xpath('//div[@aria-label="Color"]')
    color.click()
    transparent = wd.find_element_by_xpath('//a[@aria-label="Transparent"]')
    transparent.click()
    # get image thumbnail results 
    thumbnail_result = wd.find_element_by_xpath('//img[@class="rg_i Q4LuWd"]')
    thumbnail_result.click()
    time.sleep(delay)
    actual_images = wd.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')
    if actual_images.get_attribute('src') and 'http' in actual_images.get_attribute('src'):
        return actual_images.get_attribute('src')
            
def download_image(url,name):
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # file_name = f"PNG-LOGOS_{dt_string}"
    urllib.request.urlretrieve(url,f"{name}.png")

with open ('brands.csv') as f:
    head = next(f)
    delim = "," 
    head = filter(None, head.rstrip().split(delim))
    reader = csv.reader(f,delimiter=delim, skipinitialspace=True)
    zipped = zip(*reader)
    strings = next(zipped)
    for brand in strings:
        try:
            url = search_imag(brand)
            image_url = get_image_url(wd,1,url)
            print(image_url)
            download_image(image_url,brand)
        except:
            continue    
                          
wd.quit()                   


