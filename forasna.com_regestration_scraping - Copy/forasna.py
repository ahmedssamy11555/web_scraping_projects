from selenium import webdriver
import requests
import pandas as pd
import time
from selenium.webdriver.support.ui import Select

PATH ="chromedriver.exe"
wd = webdriver.Chrome(executable_path = PATH)
wd.get('https://phyllis.nl/Browse/Standard/ECN-Phyllis')
wd.maximize_window()


email = wd.find_element_by_xpath('//input[@id="email"]')
password = wd.find_element_by_xpath('//input[@id="password"]')

email.send_keys('ifarid@flykitesurfing.com')
password.send_keys('If100278')

wd.find_element_by_xpath('//button[@id="btn-submit"]').click()
time.sleep(2)
wd.find_element_by_xpath('//*[@id="leftDropDownList"]/div/span[1]').click()
time.sleep(2)
wd.find_element_by_xpath('//*[@id="leftDropDownList"]/ul/li[1]/a').click()
time.sleep(2)

#getting all the form data
def get_data(xpath,wd):
    data_item = wd.find_elements_by_xpath(xpath)
    items = []
    for item in data_item:
        items.append(item.text)    
    return items


#unchanged
country = get_data('//select[@id="country"]/option',wd)


governate = get_data('//select[@id="governate"]/option',wd)
# area = get_data('//select[@id="area"]/option',wd)
governate = []
area = []




governate = get_data('//select[@id="governate"]/option',wd)

select = Select(wd.find_element_by_id("area"))
options_2 = select.options

select = Select(wd.find_element_by_id("governate"))
for gov in governate:
    try:
        # select.select_by_visible_text(gov).click()
        for text in select.select_by_visible_text(gov).click():
            select.select_by_index(text).click()
            area.append(select.select_by_index(index_2).text)
    
    except:
        continue

   
    


# na =  wd.find_element_by_xpath('//a[@class="select2-choice"][1]')
# na.click()
# time.sleep(2)
# nationality = get_data('//div[@class="select2-result-label"]',wd)
# education_level = get_data('//select[@id="education_level"]/option',wd)

# #Drop downs 
# select = Select(wd.find_element_by_xpath('//select[@id="education_level"]'))
# select.select_by_value("8")

# certificate = get_data('//div[@class="select2-result-label"]',wd)
# graduated_in = get_data('//select[@id="graduated_in"]/option',wd)

    
# birth_year = get_data('//select[@id="birth_year"]/option',wd)
# military_status = get_data('//select[@id="military_status"]/option',wd)
# referral = get_data('//select[@id="referral"]/option',wd)
# gender = get_data('//label[contains(@class,"btn btn-default form-label ")]',wd)
        
 
# Create Dataframe in Pandas and export to CSV (Excel)
# a = {'الدولة': country, 'المحافظة': governate, 'المنطقة': area, 'الجنسية': nationality,
# 'المستوي التعليمي': education_level, 'الكلية/المعهد':certificate, 'عام التخرج':graduated_in, 'سنة الميلاد': birth_year,
# 'النوع': gender, 'الخدمة العسكرية': military_status, 'كيف علمت عن فرصنا': referral}
# df = pd.DataFrame.from_dict(a, orient='index')
# df = df.transpose()
# df.to_csv('forasna_data2.csv', index=False,encoding='utf-8-sig')



a = {'الدولة': country, 'المحافظة': governate, 'المنطقة': area}
df = pd.DataFrame.from_dict(a, orient='index')
df = df.transpose()
df.to_csv('forasna_data3.csv', index=False,encoding='utf-8-sig')

wd.quit()
