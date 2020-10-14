# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

from parsel import Selector
import uuid
import codecs

import csv


driver = webdriver.Chrome(executable_path="/mnt/d/Automation2/chromedriver.exe")
salary_info = codecs.open('salary_average.csv', 'w', 'utf-8')
salary_info.write("experience_id;profile_id;experience_title;experience_location;average_salary;salary_by_what\n")

driver.get('https://www.glassdoor.de/profile/login_input.htm')

sleep(2)

username = driver.find_element_by_id('userEmail')

username.send_keys('userActualEmail')


sleep(3)

password = driver.find_element_by_id('userPassword')

password.send_keys('userActualPassword')

sleep(1)

cookiebut = driver.find_element_by_id('_evidon-accept-button')

cookiebut.click()


sleep(1)


log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

log_in_button.click()

sleep(1)


sleep(2)

with open("/mnt/d/Automation2/linkedin_profile_experience.csv", "r") as jobExp:

    csvReader = csv.DictReader(jobExp, delimiter=',')
    for row in csvReader:
        sleep(0.5)

        a = row["experience_title"]
        b = row["experience_location"]       

        driver.get('https://www.glassdoor.de/Geh%C3%A4lter/index.htm')
        
        
        sleep(1)
        
        try:
            job = driver.find_element_by_id("KeywordSearch")
            job.send_keys(a)
            sleep(0.5)
        except ElementClickInterceptedException:
            pass

        sleep(1)
        
        try:
            place= driver.find_element_by_id("LocationSearch")
            place.clear()
            place.send_keys(b)
            sleep(0.5)
        except ElementClickInterceptedException:
            pass

        searchJob= driver.find_element_by_id("HeroSearchButton")
        searchJob.click()
        
        try:
            cookiebutton = driver.find_element_by_id('_evidon-accept-button')
            cookiebutton.click()
        except ElementClickInterceptedException:
            pass
        sleep(1)
        
        
        
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
        sleep(1)
        try: 
            salary = driver.find_element_by_xpath('//*[@data-test="AveragePay"]').text
            print(salary)
        
            salaryWhat = driver.find_element_by_xpath('//*[@class="occMedianModule__OccMedianBasePayStyle__yearLabel"]').text
            print(salaryWhat)
        except NoSuchElementException:
            salary = ""
            salaryWhat = ""
        
        experience_title = a
        experience_location = b
        
        experience_id = ""
        profile_id = ""
        average_salary  = salary
        salary_by_what = salaryWhat
        
        salary_info.write("'{0}';'{1}';'{2}';'{3}';'{4}';'{5}'\n".format(experience_id, profile_id, experience_title, experience_location, average_salary, salary_by_what))
        salary_info.flush()
       
        
sleep(1)



