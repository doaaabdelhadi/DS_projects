# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
scraping for http://www.expoegypt.gov.eg/exporters >> this project is over on Freelancer website
Details of project 
the website contains 508 pages, each page contains 10 companies.
I want to scrap each company data into an excel sheet ( name, email, phone, city).
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(executable_path=r'H:/Programs/chromedriver.exe')

#url='http://www.expoegypt.gov.eg/exporters'

def CollectionData(driver):
    campanies_info = []


    page =driver.find_elements_by_css_selector('#page_wrapper > section:nth-child(7) > div > div > div.col-md-9')
    title_lst=[]
    city_lst=[]
    tel_lst=[]
    email_lst=[]
    url_lst=[]
                                           
    for item in page:

        titles = item.find_elements_by_class_name('co_title')
        title_lst.extend([title.text for title in titles])
        time.sleep(1)        
        urls = item.find_elements_by_link_text('المزيد من التفاصيل')
        url_lst.extend([url.get_attribute('href') for url in urls])
    for url in url_lst:
        driver.get(url)
        time.sleep(1)
        cities =driver.find_element_by_css_selector('div.continfo').text
        city_lst.append(cities)
        tels= driver.find_element_by_css_selector('#page_wrapper > section.hg_section.mtop-100 > div > form > div > div > div:nth-child(6) > div:nth-child(1) > div.companybox > div > table > tbody > tr:nth-child(3) > td').text
        tel_lst.append(tels)
        emails = driver.find_element_by_css_selector('#page_wrapper > section.hg_section.mtop-100 > div > form > div > div > div:nth-child(6) > div:nth-child(1) > div.companybox > div > table > tbody > tr:nth-child(4) > td').text
        email_lst.append(emails)
        time.sleep(1)
    campany_info={'name': title_lst, 'url': url_lst,'city':city_lst,'tel':tel_lst,'email':email_lst}
    campanies_info.append(campany_info)
    

    return(campanies_info)    
#change 5 to 509 if need to scraping all pages    
for i in range(1,5):
    page_url=f"http://www.expoegypt.gov.eg/exporters?page={int(i)}"
    
    driver.get(page_url)
    time.sleep(1)
    
    companys = CollectionData(driver)
    print(companys)


time.sleep(2)
driver.quit()
