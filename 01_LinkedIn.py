#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# prerequisite installs for Python3 (run in Anaconda3 prompt)
#pip install selenium  
#pip install parsel


# In[4]:


##### Step 1: Searching LinkedIn profiles on Google #####

# chromedriver for chrome version 79
chromedriver_path = "/mnt/d/Automation2/chromedriver.exe"

# import web driver
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

search_query = 'site:linkedin.com/in/ AND "Rhine-Waal University"'

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.get('https://www.google.de/')
sleep(1)

actions = ActionChains(driver)
actions.send_keys(search_query)
actions.send_keys(Keys.RETURN)
actions.perform()
sleep(1)

linkedin_urls_elements = driver.find_elements_by_xpath('//*[@class="rc"]/div[1]/a')
linkedin_urls = [url.get_attribute("href") for url in linkedin_urls_elements]
    
# locate submit button by_xpath
next_page = driver.find_element_by_id("pnnext")

while next_page:        
    next_page.click()
    sleep(1)
    
    linkedin_urls_elements = driver.find_elements_by_xpath('//*[@class="rc"]/div[1]/a')
    temp_linkedin_urls = [url.get_attribute("href") for url in linkedin_urls_elements]
    
    for x in temp_linkedin_urls:
      linkedin_urls.append(x)
    
    try:
        next_page = driver.find_element_by_id("pnnext")
    except:
        next_page = False 

# to print all elements within our list 
linkedin_urls        
