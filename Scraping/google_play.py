# -*- coding: utf-8 -*-
"""

@author: Doaa
"""
#imported libs

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
from selenium.common.exceptions import NoSuchElementException
#define driver
driver = webdriver.Edge('H:/Programs/MicrosoftWebDriver.exe')
#set your URL
url=''
driver.get(url)

#open all reviews
all_reviews = driver.find_element_by_xpath("//span[contains(@class,'RveJvd') and contains(text(), 'قراءة جميع المراجعات')]").click()
time.sleep(2)

#collection data.

def CollectionData():
    reviews = driver.find_elements_by_class_name('d15Mdf')

    ratting_lst=[]
    comments_lst=[]
   # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
        time.sleep(0.5)

    # Calculate new scroll height and compare with last scroll height
        try:
            more=driver.find_element_by_xpath("//span[contains(@class,'RveJvd') and contains(text(), 'عرض المزيد')]")
            more.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
                break
        last_height = new_height
    for review in reviews:
        rattings =review.find_elements_by_css_selector('div.pf5lIe div')[0].get_attribute('aria-label') 
                                #('ascii', 'ignore').encode('utf-8'
        comments= repr(review.find_elements_by_css_selector('div.UD7Dzf span')[0].text)
        ratting_lst.append(rattings)
        comments_lst.append(comments)
        


    return(list(zip(ratting_lst, comments_lst)))
df = pd.DataFrame(CollectionData(), columns =['rattings', 'comments']) 

print(df.head())  
print(df.tail())
#save data
file_name = "google_play.csv"
df.to_csv(file_name,index=False)
driver.quit()


