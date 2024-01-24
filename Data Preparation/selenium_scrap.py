from selenium import webdriver
from time import sleep
from pymongo import MongoClient
from json import dump
import pickle
from random import randint

#acces to mongo db
client = MongoClient()
coll = client.get_database('pi').get_collection('dataBrut')
data = list(coll.find())

#preparing a list containing the id, url , and the things to scrap
links = [{'id':str(item['_id']),'url':item['url'], 'followers':0, 'recomendations':[], "certifs":[]} for item in data ]
company_urls = []


#connectiog to linkedin 
driver = webdriver.Chrome("chromedriver_linux64/chromedriver") 
driver.get('https://www.linkedin.com') 
identif = driver.find_element_by_css_selector('a[data-tracking-control-name="guest_homepage-basic_nav-header-signin"]') 
identif.click()
sleep(1)
username  = driver.find_element_by_id('username')                                                              
username.send_keys('chnenaouighofrane@gmail.com')                                                                     
passw = driver.find_element_by_id('password')                                                                  
passw.send_keys('71602429') 
sleep(1)
submit = driver.find_element_by_css_selector('btn__primary--large from__button--floating') 
submit.click()


#looping urls and scrapping data
for i in range(1800,1802):
    try:
        driver.get(links[i]['url'])

        #followers scraping
        folowers= driver.find_element_by_css_selector('li.inline-block span.t-16.t-black.t-normal')
        links[i]['followers'] = folowers.text

        #recommendation scrapping
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        try:
            recom_section = driver.find_element_by_css_selector('.pv-recommendations-section')
            buttons = recom_section.find_elements_by_css_selector('.no-wrap .ember-view')
            driver.execute_script("window.scrollTo(0, "+str(buttons[0].location['y']-400)+");")
            sleep(0.5)
            buttons[0].click()
            try:
                plus_rec = recom_section.find_element_by_css_selector('.pv-recommendations-section .artdeco-button--fluid')
                driver.execute_script("window.scrollTo(0, "+str(plus_rec.location['y']-400)+");")
                plus_rec.click()
            except:
                pass
            learn_more = recom_section.find_elements_by_css_selector('.pv-recommendations-section .lt-line-clamp__more')
            for element in learn_more:
                try :
                    driver.execute_script("window.scrollTo(0, "+str(element.location['y']-300)+");")
                    element.click()
                except:
                    pass
            texts = recom_section.find_elements_by_css_selector('.pv-recommendation-entity__text .ember-view')
            links[i]['recomendations'] = list(map(lambda x: x.text, texts))
        except:
            pass    

        #certifs scrapping
        try :
            try :
                button_cert = driver.find_element_by_css_selector('#certifications-section button.pv-profile-section__see-more-inline')
                driver.execute_script("window.scrollTo(0, "+str(button_cert.location['y']-300)+");")
                button_cert.click()
            except :
                pass
            certifs_company = list(map(lambda x: (x.text.split("\n")[0],x.text.split("\n")[2]) ,driver.find_elements_by_css_selector("#certifications-section div.pv-certifications__summary-info") )) 
            links[i]['certifs']=certifs_company
        except :
            pass
        #jobs scrapping
        try :
            try :
                button = driver.find_element_by_css_selector('#experience-section button.pv-profile-section__see-more-inline ')
                driver.execute_script("window.scrollTo(0, "+str(button.location['y']-300)+");")
                button.click()
            except :
                pass    
            company_urls.append( list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_css_selector('#experience-section a[data-control-name="background_details_company"]'))))
        except:
            pass    
        print(links[i])
        print(i)
        sleep(randint(3,7))
    except :
        print("link not available")    

with open('scrapping1800-10000.json', 'w', encoding='utf8') as file:
    dump(links[1800:10000], file, ensure_ascii=False)   

with open('jobs1800-10000.pckl', 'wb') as file:
    pickle.dump(company_urls, file)   

