from selenium import webdriver
import re
import time
import pandas as pd

#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument("--lang=en")
options.add_argument("--lang=ar")

driver = webdriver.Chrome(chrome_options=options,executable_path=r'H:/Programs/driver/chromedriver.exe')

url="https://apps.apple.com/sa/app/nana-%D9%86%D8%B9%D9%86%D8%A7%D8%B9/id1055344588"

driver.get(url)
## go to Ipad
##time.sleep(2)
##all_reviews = driver.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div/div[2]/section[2]/div[1]/nav/ul/li[2]/a').click()

driver.maximize_window()
time.sleep(2)
all_reviews = driver.find_element_by_link_text('See All').click()

time.sleep(2)

def CollectionData():
    rating_lst=[]
    comments_lst=[]
  
    while True :
          last_height = driver.execute_script("return document.body.scrollHeight")
          driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

          ratings= driver.find_elements_by_class_name('we-customer-review__rating') 
          rating_lst.extend([rating.get_attribute('aria-label') for rating in ratings])
          comments =driver.find_elements_by_css_selector('.ember-view > p:nth-child(1)')

          comments_lst.extend([comment.text for comment in comments])  
  
          time.sleep(1)
          new_height = driver.execute_script("return document.body.scrollHeight")
          if last_height == new_height:
              break
  
    return(list(zip(rating_lst, comments_lst)))
      
df = pd.DataFrame(CollectionData(), columns =['ratings', 'comments']) 
  
print(df.head())  
print(df.tail())
file_name = "iPad.csv"
df.to_csv(file_name, encoding='utf-8',index=False)

driver.close()