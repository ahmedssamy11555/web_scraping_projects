from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import datetime
import os
from threading import Thread
import logging
import sys
import time
import urllib
import ssl

Tk().withdraw()
csv_file_name = askopenfilename(title = "Select a File")
THREADS = int(input('Number of browsers: '))
images_per_brand = int(input('Number of downloaded images per brand: '))
try:
    brands = [x.strip() for x in open(csv_file_name, 'r', encoding='utf8').readlines()]
except:
    brands = [x.strip() for x in open(csv_file_name, 'r', encoding='latin-1').readlines()]

BASE_URL = 'https://www.google.com.eg/search?q=QUERY&tbm=isch&hl=en&tbs=ic:trans'
HEADLESS = False

def googleImages(browser, brand):
    global n
    images = []
    browser.get(BASE_URL.replace('QUERY', f'{brand.replace("&", "%26")} logo'))
    try:
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//span/div/div/div')))
        except:
            return False
        i = 0
        while len(images) < images_per_brand:
            imageURL = 'data:image'
            trials = 0
            browser.find_elements(By.XPATH, '//span/div/div/div')[i].click()
            i += 1
            while 'data:image' in imageURL or '.jpg' in imageURL:
                possible_urls = browser.find_elements(By.XPATH, f'//div/div/a/img')
                for possible_url in possible_urls:
                    try:
                        imageURL = possible_url.get_attribute('src')
                        if 'data:image' not in imageURL and imageURL not in images:
                            images.append(imageURL)
                            break
                    except:
                        pass

                time.sleep(1)
                trials += 1
                if trials == 10:
                    if len(images) < images_per_brand:
                        break
                    if images:
                        return images
                    return False
        return images
    except Exception:
        if images:
            return images
        return False

browsers = []
def FRBrowser(curBrowser=None, complete=False):
    global browsers
    if curBrowser == 'STOPALL':
        for browser in browsers:
            browser[0].close()
        browsers = []
        return

    if complete == True:
        for br in browsers:
            if curBrowser == br[0]:
                br[1] = False
        return True

    for browser in browsers:
        if browser[1] == False:
            browser[1] = True
            return browser[0]

    if THREADS > len(browsers):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        if HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('window-size=1920x1080')
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        browsers.append([browser, True])
        return browser

date_now = datetime.datetime.now()
os.makedirs(os.getcwd() + os.sep + f"images_{date_now.strftime('%Y-%m-%d_%H-%M')}", exist_ok=True)

total = 0
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
ssl._create_default_https_context = ssl._create_unverified_context

def saveImage(brand, url, n):
    global total
    location = os.getcwd() + os.sep + f"images_{date_now.strftime('%Y-%m-%d_%H-%M')}" + os.sep + brand.lower().replace('/', '-').replace('\\', '-')
    location = location.replace('..', '.').replace(' ', '-') + f'_{n}' + '.png'
    location = location.replace('|', '').replace('--', '-').replace('*', '').replace('"', '').replace("'", '')
    try:
        urllib.request.urlretrieve(url, location)
    except Exception as err:
        print(f'{url} ERROR {err}')
        writeError(brand)
        return
    
    logger.info(f'[DOWNLOADER] [{total} / {str(len(brands))}] {brand} downloaded successfully.')

retried = []
retry_queue = []
def writeError(brand, url=''):
    if brand not in retried:
        retried.append(brand)
        retry_queue.append(brand)
    else:
        try:
            with open(f"failed-brands_{date_now.strftime('%Y-%m-%d_%H-%M')}.txt", 'a+', encoding='latin-1') as file:
                file.write(f'{brand} ({url})\n')
        except:
            with open(f"failed-brands_{date_now.strftime('%Y-%m-%d_%H-%M')}.txt", 'a+', encoding='utf8') as file:
                file.write(f'{brand} ({url})\n')

def initialize_logging():
    global logger
    logging.basicConfig(filename="google-images.log", format='%(asctime)s [%(levelname)s] %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Scraper started.')
initialize_logging()

def startThread(brand):
    global total
    browser = FRBrowser()
    try:
        if browser:
            imageURLs = googleImages(browser, brand)
            FRBrowser(browser, True)
            if imageURLs:
                n = 1
                for image in imageURLs:
                    saveImage(brand, image, n)
                    n += 1
                total += 1
            else:
                writeError(brand)
    except:
        writeError(brand)

threads = []
for brand in brands:
    try:
        if not brand:
            continue
        thread = Thread(target=startThread, args=(brand,))
        threads.append(thread)
        thread.start()
        if len(threads) == THREADS:
            for thread in threads:
                thread.join()
            threads = []
    except:
        writeError(brand)
    
    if len(retry_queue):
        for brand in retry_queue:
            try:
                thread = Thread(target=startThread, args=(brand,))
                threads.append(thread)
                thread.start()
                if len(threads) == THREADS:
                    for thread in threads:
                        thread.join()
                    threads = []
            except:
                writeError(brand)
        retry_queue = []

for thread in threads:
    thread.join()

FRBrowser('STOPALL')
