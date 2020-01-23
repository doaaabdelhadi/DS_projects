from selenium import webdriver
import re
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument("--lang=en")
options.add_argument("--lang=ar")

driver = webdriver.Chrome(chrome_options=options,executable_path=r'H:/Programs/driver/chromedriver.exe')
##set_url
url=""

driver.get(url)

## if you need to go to Ipad uncommunt two lines
# time.sleep(2)
# ipad = driver.find_element_by_xpath('/html/body/div[7]/main/div/div/div/div[2]/section[2]/div[1]/nav/ul/li[2]/a').click()

driver.maximize_window()
time.sleep(2)
#open all reviews
all_reviews = driver.find_element_by_link_text('See All').click()

time.sleep(2)

def CollectionData():
    rating_lst=[]
    comments_lst=[]
# Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
        time.sleep(1.2)

    # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
                break
        last_height = new_height
        
    ratings= driver.find_elements_by_class_name('we-customer-review__rating') 
    rating_lst.extend([rating.get_attribute('aria-label') for rating in ratings])
    comments =driver.find_elements_by_class_name('we-clamp')
    comments_lst.extend([comment.text for comment in comments])  


  
    return(list(zip(rating_lst, comments_lst)))
      
df = pd.DataFrame(CollectionData(), columns =['ratings', 'comments']) 
  
print(df.head())  
print(df.tail())
file_name = "iphone.csv"
#comment file_name ("iphone.csv") if will select ipad and uncomment ipad.csv.
#file_name = "ipad.csv"
df.to_csv(file_name, encoding='utf-8',index=False)

driver.close()
