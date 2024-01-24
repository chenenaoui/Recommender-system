import json
import pickle
import os
from selenium import webdriver
from time import sleep
from random import randint

#prepare counter_urls : 
if 'comp_treated.pckl' not in os.listdir():
    treated_url = set()
    with open ("comp_treated.pckl", 'wb') as file :
        pickle.dump(treated_url, file)

if 'all_companies.pckl' not in os.listdir():
    companies = []
    with open ("all_companies.pckl", 'wb') as file :
        pickle.dump([], file)


with open ("comp_treated.pckl", 'rb') as file :
    treated_url= pickle.load(file)

with open ("all_companies.pckl", 'rb') as file :
    companies= pickle.load(file)    

#load jobs urls: 
urls = set()
for file_path in list(filter(lambda x: "jobs" in x, os.listdir())):
    with open(file_path, 'rb') as file:
        for row in pickle.load(file):
            for item in row:
                if 'search/results/' not in item: 
                    urls.add(item)


# setting selenium

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
submit = driver.find_element_by_css_selector('button[data-control-urn="login-submit"]') 
submit.click()

#start scrapping
print("companies remaning to scrap : %d "%(len(urls)-len(treated_url)))
i=0
treated_tompon = []
comp = []
for url in list(urls):
    try : 
        if url not in treated_url:
            tmp = {'name':"", "url":url,"foll":"","info":""}
            driver.get(url+"about/")

            tmp['name']= driver.find_element_by_css_selector('h1.org-top-card-summary__title.t-24.t-black span').text 
            tmp['foll'] = driver.find_element_by_css_selector('.org-top-card-summary-info-list.t-14.t-black--light').text
            tmp['info']=driver.find_element_by_css_selector('.overflow-hidden').text 

            print(tmp)
            i += 1
            print(i)

            comp.append(tmp)
            treated_tompon.append(url)
            sleep(randint(4,8))
    except: 
        print("not available")        



#saving treated data:

for i in treated_tompon:
    treated_url.add(i)

with open ("comp_treated.pckl", 'wb') as file :
    pickle.dump(treated_url, file)

#saving scrapping :

for i in comp:
    companies.append(i)

with open ("all_companies.pckl", 'wb') as file :
    pickle.dump(companies, file)


print(len(treated_tompon))
print(len(treated_url))                    