
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

url ="https://www.facebook.com/"
chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications": 2}

chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path=r'H:/Programs/chromedriver.exe',chrome_options=chrome_options)


driver.get(url) ## open url
email = driver.find_element_by_name('email')

email.send_keys("enter-eamil")

password =driver.find_element_by_name('pass')
password.send_keys("enter password")
driver.find_element_by_xpath("//input[@value='Log In']").click()
time.sleep(0.5)
driver.get('https://www.facebook.com/groups/id/')
driver.maximize_window()

time.sleep(0.5)

driver.find_element_by_link_text('Members').click()
time.sleep(1)
element=driver.find_element_by_id('groupsMemberSection_recently_joined')
driver.execute_script("arguments[0].scrollIntoView();", element)
m_lsts=[]
members_link=[]
last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    try:
        classofmembers=element.find_elements_by_css_selector('div._60ri')
        m_lsts.extend([member.find_element_by_tag_name('a') for member in classofmembers])
        members_link.extend([links.get_attribute('href') for links in m_lsts])
    except NoSuchElementException:
        pass
    time.sleep(.5)
  
    # Wait to load page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
                break
    last_height = new_height
print(len(members_link))
