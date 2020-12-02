#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pychrome #in command line type - pip install pychrome
import pandas as pd #pandas library
import numpy as np
from selenium import webdriver #pip install selenium
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=8000")

from pymongo import MongoClient 
client = MongoClient() 
client = MongoClient("localhost", 27017)
auto_complete = client.Google_autocomplete

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# In[13]:


driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
dev_tools = pychrome.Browser(url="http://localhost:8000")
tab = dev_tools.list_tab()[0]
tab.start()


# In[19]:


language_df = pd.DataFrame()
language_df['English_language'] = ['English','Hindi','Bengali','Telugu','Marathi','Tamil','Gujarati','Kannada','Malyalam','Punjabi']
language_df['Actual_language'] = ['English','हिन्दी','বাংলা','తెలుగు','मराठी','தமிழ்','ગુજરાતી','ಕನ್ನಡ','മലയാള','ਪੰਜਾਬੀ']
print(language_df)


# In[15]:


letters_df = pd.DataFrame()
letters_df['Language'] = ['English','हिन्दी']
letters_df['Letters'] = [['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
                        ["क","ख","ग","घ","ड","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ल","व","श","ष","स","ह","ञ"]]
print(letters_df)


# In[16]:


coordinates = pd.read_csv('Final_csv_for_Looping.csv',converters={'Languages':eval})
coordinates['Languages'] =  [['हिन्दी','English'],['हिन्दी','English'],['हिन्दी','English'],['हिन्दी','English'],['हिन्दी','English'],['हिन्दी','English']]
coordinates.head()


# In[17]:


for i in range(len(coordinates)):
    json_language = {}
    driver.get("https://www.google.co.in/search?q=a")
    time.sleep(3)
    tab.call_method("Network.enable", _timeout=20)
    tab.call_method("Browser.grantPermissions",permissions=['geolocation'])
    tab.call_method("Emulation.setGeolocationOverride",latitude=coordinates.iloc[i,1],longitude=coordinates.iloc[i,2]
                    ,accuracy=100)
    time.sleep(20)
    bodyText = driver.find_element_by_tag_name('body').text
    if 'Use precise location' in bodyText:
        driver.find_element_by_xpath("//a[text()='Use precise location']").click()
    else:
        driver.find_element_by_xpath("//a[text()='Update location']").click()
    time.sleep(3)#do not forget to change
    driver.get(str(coordinates.iloc[i,4]))
    time.sleep(3)
    for each_language in range(len(coordinates.iloc[i,3])):
        json_letters = {}
        xpath = "//a[text()='" + str(coordinates.iloc[i,3][each_language]) + "']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(10)
        letters_list = letters_df[letters_df['Language']==coordinates.loc[i,'Languages'][each_language]]['Letters'].values[0]
        search_field = driver.find_element_by_name("q")
        for j in range(len(letters_list)):
            search_field = driver.find_element_by_name("q")
            autocomplete_list_of_a_letter = []
            search_field.send_keys(str(letters_list[j]))
            time.sleep(2)#do not forget to change it
            for loop in range(1,11):
                try:
                    li_items = driver.find_element_by_xpath('//*/ul/li[%d]/div/div[2]/div[1]' %(loop)).text
                    autocomplete_list_of_a_letter.append(li_items)
                except NoSuchElementException:
                    time.sleep(10)
                    try:
                        li_items = driver.find_element_by_xpath('//*/ul/li[%d]/div/div[2]/div[1]' %(loop)).text
                        autocomplete_list_of_a_letter.append(li_items)
                    except NoSuchElementException:
                        for inner_loop in range(loop-1,10):
                            autocomplete_list_of_a_letter.append(None)
                        break
            driver.find_element_by_name("q").clear()
            json_letters[str(letters_list[j])] = autocomplete_list_of_a_letter
        json_language[str(coordinates.loc[i,'Languages'][each_language])] = json_letters
        ac = ActionChains(driver)
        ac.move_to_element(search_field).move_by_offset(300,0).click().perform()
        time.sleep(10)
    rec={
        "City": coordinates.iloc[i,0],
        "date": str(datetime.datetime.now()).split('.')[0],
        "Autocomplete": json_language
    }
    auto_complete.India.insert_one(rec)
    time.sleep(10)

