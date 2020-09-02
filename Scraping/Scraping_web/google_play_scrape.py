# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 16:09:11 2020

@author: Doaa
"""

#import libs
import time
from selenium import webdriver
import pandas as pd 
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException
#import re
#import numpy as np
#from langdetect import detect


page_load_timeout = 1
## luach drvier
def drive_Edge():
    #driver = webdriver.Edge(executable_path= r'C:/Windows/SysWOW64/MicrosoftWebDriver.exe')
    #driver=webdriver.Chrome(executable_path=r'H:/Programs/driver/chromedriver.exe')
    driver=webdriver.Firefox(executable_path='C:/Users/Doaa/Desktop/geckodriver')
    return(driver)
 ##open url   
def get_url(page_url, driver):
    url=page_url+'&showAllReviews=true'
    driver.get(url)
    time.sleep(page_load_timeout)
    return True
## info of App    
def App_Info(driver):
    info =driver.find_element_by_class_name('sIskre')
    name =info.find_element_by_css_selector('h1.AHFaub span').text
    category= info.find_elements_by_css_selector('div.jdjqLd div.ZVWMWc div.qQKdcc span')[1].text
    info_lst=[name,category]
    return(info_lst)
    
def scroll_more(driver):
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
        reviews = driver.find_elements_by_class_name('d15Mdf')
    return(reviews)
        
def data_scraping(reviews,driver):
    #lst of info 
    ratting_lst=[]
    comments_lst=[]
    date_lst=[]
    comments_ratting_lst=[]
    user_lst=[]
    
    for review in reviews:
        rattings =review.find_elements_by_css_selector('div.pf5lIe div')[0].get_attribute('aria-label')
        
        ratting_lst.append(rattings)
        comments=(review.find_elements_by_css_selector('div.UD7Dzf span')[0].text)
        comments_lst.append(comments)
    
        comments_ratting =repr(review.find_elements_by_css_selector('div.jUL89d.y92BAb')[0].text)
        comments_ratting_lst.append(comments_ratting)
    
        review_date =review.find_elements_by_css_selector('span.p2TkOb')[0].text
        date_lst.append(review_date)
        
        user =review.find_elements_by_css_selector('span.X43Kjb')[0].text
        user_lst.append(user)
        try: 
            but=review.find_element_by_css_selector('button.LkLjZd.ScJHi.OzU4dc')
            driver.execute_script("arguments[0].click();", but)
              
            comments=(review.find_elements_by_css_selector('div.UD7Dzf span[jsname="fbQN7e"]'))
            for comment in comments:
                comments_lst.append(comment.text)
       
        except NoSuchElementException:
            comments=(review.find_elements_by_css_selector('div.UD7Dzf span')[0].text)
            comments_lst.append(comments)
            

    print('Please Waiting....')
    return(list(zip(ratting_lst, comments_lst,date_lst,comments_ratting_lst,user_lst)))
    
    
    
## extract ratting number google
#def ratting_google(lst):
#    res=[(sub.split(' ')[3]) for sub in lst]
#    return(res)




def save_data(data,app_info):
    print(len(data))
    df = pd.DataFrame(data, columns =['rattings', 'comments','date','comments_ratting','user']) 
    file_name = app_info[0] +".csv"
    df.to_csv(file_name,index=False,encoding='utf-8') 
    df.to_json(app_info[0]+'.json')
    with open(app_info[0]+'.txt', 'w') as f:
        for item in app_info:
            f.write("%s\n" % item)

    return(True)
    
   
    
def run_scraping():        
    try:           
        driver =drive_Edge() 
        url='https://play.google.com/store/apps/details?id=com.mcdonalds.mobileapp&hl=ar'
        get_url(url, driver)       
        Info_of_app= App_Info(driver)
        time.sleep(page_load_timeout)
        reviews=scroll_more(driver)
        time.sleep(page_load_timeout*2)
        
        data =data_scraping(reviews,driver)
        save_data(data,Info_of_app)
        driver.quit()
        print("Data of is ready to use.")
    except (NoSuchWindowException,NoSuchElementException):
         driver.quit()
        
    return(True)
run_scraping()    
#url='https://play.google.com/store/apps/details?id=com.fakahany&hl=ar'
#url='https://play.google.com/store/apps/details?id=com.todoorstep.store&hl=ar'
#url='https://play.google.com/store/apps/details?id=com.zadfresh.zadfresh&hl=ar'
#url='https://play.google.com/store/apps/details?id=com.app.danube&hl=ar'
#url='https://play.google.com/store/apps/details?id=ibtikar.haseel.user&hl=ar'
#url='https://play.google.com/store/apps/details?id=com.akio.avokado&hl=ar'
