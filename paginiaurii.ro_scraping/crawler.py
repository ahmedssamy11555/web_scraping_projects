
from bs4 import BeautifulSoup
import requests
import io
import csv
from itertools import zip_longest
import pandas as pd
import time
from fake_useragent import UserAgent


ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}




proxies = {
  'http://cefege:kZxSgVUN@07.175.236.152:4444',
  'http://cefege:kZxSgVUN@108.174.49.148:4444',
  'http://cefege:kZxSgVUN@138.128.16.196:4444',
  'http://cefege:kZxSgVUN@138.229.100.134:4444',
 ' http://cefege:kZxSgVUN@139.180.229.84:4444'
  }




page_number = 1

company = []
links = []
address = []
telephone = []
email = []
opens = []
description = []
contacts = []
Cod_Fiscal =[]
product_service = []
key_words = []
activity = []
service_area = []
opening_hours = []
payment_method = []
company_logo = []
photo_and_vid_gallary =[]


def get_companies_url(url):
  r = requests.get(url,headers=header)
  return BeautifulSoup(r.text,'html.parser')

#geting all companies urls from the website and 
while True:
  website = f"https://www.paginiaurii.ro/firmy/-/q_consultan%C5%A3%C4%83+%C3%AEn+afaceri+%C5%9Fi+finan%C5%A3e/{page_number}/"
  root = 'https://www.paginiaurii.ro/'

  soup = get_companies_url(website)

  page_limit = soup.find("div",id="what-where-line").text

  page_numbers_limit = [int(word) for word in page_limit.split() if word.isdigit()]
  if (page_number> page_numbers_limit[0]//20):
      print("page ended")
      break


  companies = soup.find_all("h2", {"class":"item-heading"})


  for i in range(len(companies)):
      company.append(companies[i].text.strip())
      links.append(f"{root}{companies[i].find('a').attrs['href']}")
  page_number +=1
  print(f"page number {page_number}")

# accesing every website url and try to extract the data form it



def get_company_data(link):
  global page
  try:
      for proxy in proxies:
          try:
              page = requests.get(
              link, proxies={"http": proxy, "https": proxy},timeout=2,headers=header)
          
              # Prints Proxy server IP address if proxy is alive.
              print("Status OK, Output:", page.status_code)
          
          except :
              print('faild')
              pass
      return BeautifulSoup(page.text,'html.parser')      
  except:
      print('All the proxies not working')
      pass         
    


  for link in links:
    try:
      soup = get_company_data(link)

      #getting the logo

      logo = soup.find("div",class_="col3 company-logo")
      if logo is not None:
        company_logo.append(logo.img.attrs['src'])
      else:
        company_logo.append(" ")

      #getting the address
      addreses = soup.find('li',{"class":"address"})
      if addreses is not None:
        address.append(addreses.text)
      else:
        address.append(' ')  
      
      #getting the comany telephone
      telephones = soup.find('li',{"itemprop":"telephone"})
      if telephones is not None:
        telephone.append(telephones.text)
      else:
        telephone.append(' ')  
      
      #getting the company email
      emails = soup.find('a',{"class":"t-c","data-ta":"EmailClick"})
      if emails is not None:
        email.append(emails.text)
      else:
        email.append(' ')  
      #getting the comany opeing time
      opening = soup.find("li",class_="open")
      if opening is not None:
        opens.append(opening.text.strip())
      else:
        opens.append(' ') 
      
      #getting the company descripton
      descriptions = soup.find('section',id="description")
      if descriptions is not None:
          description.append(descriptions.text.strip())
      else:
          description.append(" ")

      #Gettitng contacts

      contact = soup.find("section",id="contacts")
      if contact is not None:
          contacts.append(contact.ul.text.strip())
      else:
          contacts.append(" ")      

      #getting code fiscal

      code = soup.find("section",id="vat-id")
      if code is not None:
        Cod_Fiscal.append(code.p.text[12:].strip())
      else:
        Cod_Fiscal.append(" ")  

      #getting products name
      products = soup.find("section",id="product_service")
      if products is not None:
        product_service.append(products.ul.text.strip())
      else:
        product_service.append(" ")  

      #getting key words

      keyword = soup.find("section",id="other_products")
      if keyword is not None:
        key_words.append(keyword.text.strip()[15:])
      else:
        key_words.append(" ") 

      #getting activities

      activities = soup.find("section",id="activity")
      if activities is not None:
        activity.append(activities.a.text.strip())
      else:
        activity.append(" ")

      #getting service area
      service_areas = soup.find("section", id="service_area")  
      if service_areas is not None:
        service_area.append(service_areas.text[15:].strip())
      else:
        service_area.append(" ")

      #getting company open hour
      open_hour = soup.find("section", id="opening-hours")  
      if open_hour is not None:
        opening_hours.append(open_hour.table.text)
      else:
        opening_hours.append(" ")     

      #geting the company payments
        
      payment_meth = soup.find("section", id="payment-method")  
      if payment_meth is not None:
        payment_method.append(payment_meth.p.text)
      else:
        payment_method.append(" ") 
      

      #getting the company photo and video
      photo = soup.find("ul",calss_="gallery-foto-inner")
      if photo is not None:
          photo_and_vid_gallary.append(photo.li.a.attrs['href'])
      else:
          photo_and_vid_gallary.append(" ")
      print(link)
    except:
        print('you need new proxies')
        pass
#Exctracting the data at csv file

df =pd.DataFrame({"company":company,"links":links,"address":address,"telephone":telephone,"email":email,"open":open,"description":description,"contacts":contacts,
"Cod_Fiscal":Cod_Fiscal,"product_service":product_service,"key_words":key_words,"activity":activity,"service_area":service_area,"opening_hours":opening_hours,
"payment_method":payment_method,"company_logo":company_logo,"photo_and_vid_gallary":photo_and_vid_gallary})


df.to_csv("data_scraping2.csv", header=True, index=False, encoding='utf_8_sig')






