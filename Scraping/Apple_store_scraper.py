# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:34:01 2020

@author: Doaa
"""

#import libs
import time
from selenium import webdriver
import pandas as pd 
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
#prefs = {"profile.managed_default_content_settings.images": 2}
#chrome_options.add_experimental_option("prefs", prefs)
#driver.delete_all_cookies()

def driver_chrome():
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'H:/Programs/driver/chromedriver.exe')
    
    return(driver)


def get_url(url,driver):
    driver.get(url)
    return True
    

def App_Info(driver) :
    info = driver.find_element_by_tag_name('header')
    name = driver.find_elements_by_css_selector('h1.product-header__title.app-header__title')[0].text.split('+')[0]
    all_info=info.find_elements_by_tag_name('ul.inline-list.inline-list--mobile-compact li')
    App_inf=[item.text for item in all_info ]
    App_inf.append(name)
    
    #App_info={"name":name,"category":all_info[0].text,"rating":all_info[1].text,"paided":all_info[2].text}
    return(App_inf)

def scroll_more(driver):
    SCROLL_PAUSE_TIME=1.2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
                break
        last_height = new_height

    
    return(True)

def data_scraping(driver):
    rating_lst=[]
    comments_lst=[]
    users_lst=[]
    dates_lst=[]
        
    ratings= driver.find_elements_by_class_name('we-customer-review__rating') 
    rating_lst.extend([rating.get_attribute('aria-label') for rating in ratings])
    comments =driver.find_elements_by_class_name('we-clamp')
    comments_lst.extend([comment.text for comment in comments])
    users=driver.find_elements_by_css_selector('span.we-truncate.we-truncate--single-line.ember-view.we-customer-review__user')
    users_lst.extend([user.text for user in users])
    dates=driver.find_elements_by_tag_name('time')
    dates_lst.extend([date.text for date in dates])

  
    return(list(zip(rating_lst, comments_lst,dates_lst,users_lst)))
def save_data(data,app_info):
    print(len(data))
    df = pd.DataFrame(data, columns =['Rattings', 'Comments','Date','User']) 
    file_name = app_info[-1] +".csv"
    df.to_csv(file_name,index=False,encoding='utf-8') 
    df.to_json(app_info[-1]+'.json')
    with open(app_info[-1]+'.txt', 'w') as f:
        for item in app_info:
            f.write("%s\n" % item)

    return(True)
    
    

def run_scraping():
    try:
        page_load_timeout=5
        
        driver =driver_chrome() 
        driver.maximize_window()

        
        url='https://apps.apple.com/eg/app/%D9%81%D9%83%D9%87%D8%A7%D9%86%D9%8A-fakahany/id1260428744'
        
        get_url(url, driver)       
        Info_of_app= App_Info(driver)
            
        time.sleep(page_load_timeout)
        all_reviews = driver.find_element_by_link_text('See All').get_attribute('href')
        print(all_reviews)
        url_2= url +'#see-all/reviews'
        if all_reviews == url_2:
            #all_reviews.click()
            get_url(url_2, driver)       
            time.sleep(page_load_timeout)
            scroll_more(driver)
            time.sleep(page_load_timeout)
                
            data =data_scraping(driver)
            if len(data) != 0:
                 save_data(data,Info_of_app)
                 print("Data of is ready to use.")
        else:
            print(Info_of_app)
            print("There aren't reviews!!!!")
        driver.quit()
    except (NoSuchWindowException,NoSuchElementException):
         driver.quit()

        
    return(True)
run_scraping()  
#"https://apps.apple.com/sa/app/nana-%D9%86%D8%B9%D9%86%D8%A7%D8%B9/id1055344588"  
#'https://apps.apple.com/eg/app/%D9%81%D9%83%D9%87%D8%A7%D9%86%D9%8A-fakahany/id1260428744'
#"https://apps.apple.com/eg/app/%D8%AD%D8%B5%D9%8A%D9%84-haseel/id1338447528"
#"https://apps.apple.com/eg/app/lilbab-%D9%84%D9%84%D8%A8%D8%A7%D8%A8/id1059989053"