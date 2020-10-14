

##### Step 2: Scraping LinkedIn profiles #####

# chromedriver for chrome version 79
chromedriver_path = "/mnt/d/Automation2/chromedriver.exe"

# import web driver
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from parsel import Selector
import uuid
import codecs

try:
    driver
except NameError:
    print("well, chrome driver WASN'T defined after all!")
    driver = webdriver.Chrome(executable_path=chromedriver_path)
else:
    print("sure, chrome driver was defined.")
    

furls = open("profile_urls_most_complete.csv", "r")
linkedin_basic_profile = codecs.open('linkedin_basic_profile.csv', 'w', 'utf-8')
linkedin_profile_experience = codecs.open('linkedin_profile_experience.csv', 'w', 'utf-8')
linkedin_profile_experience_position = codecs.open('linkedin_profile_experience_position.csv', 'w', 'utf-8')
linkedin_profile_education = codecs.open('linkedin_profile_education.csv', 'w', 'utf-8')
linkedin_profile_languages = codecs.open('linkedin_profile_languages.csv', 'w', 'utf-8')

# write file columns
linkedin_basic_profile.write("profile_id;name;linkedin_url;location;headline;about;connections;patents;projects;awards;groups;volunteering;certifications\n")
linkedin_profile_experience.write("experience_id;profile_id;experience_title;experience_second_title;experience_start_date;experience_end_date;experience_duration;experience_location\n")
linkedin_profile_experience_position.write("experience_position_id;experience_id;position_title;position_second_title;position_start_date;position_end_date;position_duration;position_location\n")
linkedin_profile_education.write("education_id;profile_id;education_title;education_degree_title;education_field_of_study;education_start_date;education_end_date;education_duration\n")
linkedin_profile_languages.write("profile_id;language_title;language_level\n")

# For loop to iterate over each URL in the list
for linkedin_url in furls:

    
    # translate profiles into English?
    translate = True
    
    # passing the LinkedIn authwall with Google Translate :D
    linkedin_url_alt = 'https://translate.google.com/translate?hl=en&sl=auto&tl=en&u=' + linkedin_url
    
    if translate == False:
        linkedin_url_alt = linkedin_url_alt + '&anno=2'      

    successful = False
    errorCount = 0
    current_url = linkedin_url_alt
    
    while successful == False and errorCount < 6:      
        # get the profile URL 
        driver.get(current_url)

        # add a x second pause loading each URL
        sleep(2)
        
        # switch to google translate frame
        try:
            driver.switch_to.frame("c")
        except:
            print("no google translate frame found")
        
        # captcha-alert
        try:
            captcha = driver.find_element_by_css_selector("form#captcha-form")
            print("captcha found - pls solve now!")
            sleep(60)
            errorCount = 0
        except:
            print("no captcha found")
            
        # translation-alert
        try:
            translation_alert = driver.find_element_by_css_selector("h2").get_attribute("innerText").strip()
            if translation_alert.find("The page you have attempted to translate is already in English") >= 0:
                current_url = current_url.replace("&sl=auto","&sl=de") + '&anno=2' 
        except:
            print("no translation alert found")

        # basic profile
        try:      
            name = driver.find_element_by_css_selector("h1.top-card-layout__title").get_attribute("innerText").strip()

            profile_id = uuid.uuid4()
            print('Profile: ' + name)
                        
            successful = True        
        except:
            print('not a valid profile page')
            errorCount += 1

        # valid profile detected
        if successful == True:
            
            # scroll down for lazy-loading
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
            sleep(0.5)

            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(0.5)

            # profile location
            try:
                location = driver.find_element_by_css_selector("h3.top-card-layout__first-subline span.top-card__subline-item:nth-of-type(1)").get_attribute("innerText")
                location = location.strip()
            except:
                location = ""

            # profile about
            try:
                about = driver.find_element_by_css_selector("section.summary.pp-section p:nth-of-type(1)").get_attribute("innerText")
                about = about.strip().replace('\n', ' ')   
            except:
                about = ""
                
            # profile headline
            try:
                headline = driver.find_element_by_css_selector("h2.top-card-layout__headline").get_attribute("innerText")
                headline = headline.strip().replace('\n', ' ')   
            except:
                headline = ""

            # profile languages
            try:
                language_elements = driver.find_elements_by_css_selector("ul.languages__list div.result-card__contents")

                for l in language_elements:
                    
                    language = l.find_element_by_css_selector("h3.result-card__title").get_attribute("innerText").strip()
                    level = l.find_element_by_css_selector("h4.result-card__subtitle").get_attribute("innerText").strip()
                    
                    linkedin_profile_languages.write("'{0}';'{1}';'{2}'\n".format(profile_id, language, level))
                    linkedin_profile_languages.flush()
            except:
                print("no languages")
                
            # profile connections
            try:
                connections = driver.find_element_by_css_selector("span.top-card__subline-item.top-card__subline-item--bullet").get_attribute("innerText")
                connections = connections.strip().split(" ")[0]
            except:
                connections = ""
                
            # profile patents
            try:
                patents = driver.find_elements_by_css_selector("ul.patents__list li.result-card")
                patents = len(patents)
            except:
                patents = "0"
                
            # profile projects
            try:
                projects = driver.find_elements_by_css_selector("ul.projects__list li.result-card")
                projects = len(projects)
            except:
                projects = "0"
                
            # profile awards
            try:
                awards = driver.find_elements_by_css_selector("ul.awards__list li.result-card")
                awards = len(awards)
            except:
                awards = "0"
                
            # profile groups
            try:
                groups = driver.find_elements_by_css_selector("section.groups.pp-section ul li.result-card")
                groups = len(groups)
            except:
                groups = "0"
                
            # profile volunteering
            try:
                volunteering = driver.find_elements_by_css_selector("ul.volunteering__list li.result-card")
                volunteering = len(volunteering)
            except:
                volunteering = "0"
                
            # profile certifications
            try:
                certifications = driver.find_elements_by_css_selector("ul.certifications__list li.result-card")
                certifications = len(certifications)
            except:
                certifications = "0"
                
                        
            # write basic profile information to file at once
            linkedin_basic_profile.write("'{0}';'{1}';'{2}';'{3}';'{4}';'{5}';'{6}';'{7}';'{8}';'{9}';'{10}';'{11}';'{12}'\n".format(profile_id, name, linkedin_url.strip(), location, headline, about, connections, patents, projects, awards, groups, volunteering, certifications))
            linkedin_basic_profile.flush()
            
            # experience
            try:
                experience_elements = driver.find_elements_by_css_selector("ul.experience__list li.result-card.experience-item")

                # experience

                for x in experience_elements:
                    y = x.find_element_by_css_selector("div.result-card__contents.experience-item__contents")
                    experience_id = uuid.uuid4()

                    try:                       
                        # experience_id
                        linkedin_profile_experience.write("'{0}';".format(experience_id))
                        
                        # link with profile_id
                        linkedin_profile_experience.write("'{0}';".format(profile_id))
                        
                        # experience title    
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("h3.result-card__title.experience-item__title").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")

                    try:
                        # experience secondary title
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("h4.result-card__subtitle.experience-item__subtitle").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")
                        
                    try:
                        # experience date range   
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("p.experience-item__duration time.date-range__start-date").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")
                        
                    try:
                        # experience date range   
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("p.experience-item__duration time.date-range__end-date").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")

                    try:
                        # experience duration 
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("p.experience-item__duration span.date-range__duration").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")

                    try:
                        # location
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("p.experience-item__location").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_experience.write("'';")

                    linkedin_profile_experience.write("\n")
                    linkedin_profile_experience.flush()

                
                # experience group with positions
                experience_group_elements = driver.find_elements_by_css_selector("ul.experience__list li.experience-group.experience-item")

                for x in experience_group_elements:
                    y = x.find_element_by_css_selector("div.experience-group-header__content")
                    experience_id = uuid.uuid4()
                                                          
                    try:                     
                        # experience_id
                        linkedin_profile_experience.write("'{0}';".format(experience_id))
                                                          
                        # link with profile_id
                        linkedin_profile_experience.write("'{0}';".format(profile_id))
                                                          
                        # experience title    
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("h4.experience-group-header__company").get_attribute("innerText").strip()))    
                                    
                        # experience secondary title (empty)                                 
                        linkedin_profile_experience.write("'';")
                        
                        # experience date range (empty)                                 
                        linkedin_profile_experience.write("'';")
                                                          
                        # experience date range (empty)                               
                        linkedin_profile_experience.write("'';")
                                                          
                    except:
                        print('- error experience record -')

                    try:
                        # experience duration
                        linkedin_profile_experience.write("'{0}';".format(y.find_element_by_css_selector("p.experience-group-header__duration").get_attribute("innerText").strip()))   
                                                          
                    except:
                        linkedin_profile_experience.write("'';")
                                                          

                    # location (empty)
                    linkedin_profile_experience.write("'';")
                                                          
                    linkedin_profile_experience.write("\n")
                    linkedin_profile_experience.flush()

                    experience_positions = x.find_elements_by_css_selector("ul.experience-group__positions li.result-card.experience-group-position")

                    for z in experience_positions:
                        experience_position_id = uuid.uuid4()
                                                          
                        # experience_position_id
                        linkedin_profile_experience_position.write("'{0}';".format(experience_position_id))
                        
                        # link with experience_id
                        linkedin_profile_experience_position.write("'{0}';".format(experience_id))
                                                          
                        try:
                            # position title    
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("h3.result-card__title.experience-group-position__title").get_attribute("innerText").strip())) 
                        except:
                            linkedin_profile_experience_position.write("'';")

                        try:
                            # position secondary title
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("h4.result-card__subtitle.experience-group-position__subtitle").get_attribute("innerText").strip())) 
                        except:
                            linkedin_profile_experience_position.write("'';")

                        try:
                            # position date range
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("p.experience-group-position__duration time.date-range__start-date").get_attribute("innerText").strip()))
                        except:
                            linkedin_profile_experience_position.write("'';")

                        try:
                            # position date range
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("p.experience-group-position__duration time.date-range__end-date").get_attribute("innerText").strip()))
                        except:
                            linkedin_profile_experience_position.write("'';")

                        try:
                            # position duration
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("p.experience-group-position__duration span.date-range__duration").get_attribute("innerText").strip()))
                        except:
                            linkedin_profile_experience_position.write("'';")

                        try:
                            # position location
                            linkedin_profile_experience_position.write("'{0}';".format(z.find_element_by_css_selector("p.experience-group-position__location").get_attribute("innerText").strip()))
                        except:
                            linkedin_profile_experience_position.write("'';")

                        linkedin_profile_experience_position.write("\n")
                        linkedin_profile_experience_position.flush()

            except:
                print('no experience found')

            # education 
            try:
                education_elements = driver.find_elements_by_css_selector("ul.education__list div.result-card__contents")
                                                        
                for x in education_elements:
                    education_id = uuid.uuid4()
                                                          
                    try:
                        # education_id
                        linkedin_profile_education.write("'{0}';".format(experience_id))
                                                          
                        # link with profile_id
                        linkedin_profile_education.write("'{0}';".format(profile_id))
                                                        
                        # education title
                        linkedin_profile_education.write("'{0}';".format(x.find_element_by_css_selector("h3.result-card__title").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_education.write("'';")

                    try:
                        # education degree title
                        linkedin_profile_education.write("'{0}';".format(x.find_element_by_css_selector("h4.result-card__subtitle span:nth-of-type(1)").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_education.write("'';")

                    try:
                        # education field of study title
                        linkedin_profile_education.write("'{0}';".format(x.find_element_by_css_selector("h4.result-card__subtitle span:nth-of-type(2)").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_education.write("'';")

                    try:
                        # education date range
                        linkedin_profile_education.write("'{0}';".format(x.find_element_by_css_selector("p.education__item.education__item--duration time:nth-of-type(1)").get_attribute("innerText").strip()))                               
                    except:
                        linkedin_profile_education.write("'';")

                    try:
                        # education date range
                        linkedin_profile_education.write("'{0}';".format(x.find_element_by_css_selector("p.education__item.education__item--duration time:nth-of-type(2)").get_attribute("innerText").strip()))
                    except:
                        linkedin_profile_education.write("'';")


                    linkedin_profile_education.write("\n")
                    linkedin_profile_education.flush()
            except:
                print('no education found')


           



