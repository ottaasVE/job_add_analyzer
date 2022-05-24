import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import re
import dateparser
import linkedin_functions as lf
import time
from selenium import webdriver
import chromedriver_autoinstaller

# Install chromedriver
chromedriver_autoinstaller.install()

# Creating webdriver instance
driver = webdriver.Chrome()

extraction_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
filepath = r'C:\Users\ottaas\Downloads' + '\linkedin_jobs_' + extraction_time + '.json'
print(filepath)

URL = "https://www.linkedin.com/jobs/search?keywords=%22Data%20Engineer%22&location=Norway&geoId=103819153&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
page = driver.get(URL)
time.sleep(5)

lf.scroll_to_bottom(driver)

df = pd.DataFrame({'ID':[], 'job_title':[],'url':[], 'info':[],  'key_words':[], 'html_string':[]})

src = driver.page_source

soup = BeautifulSoup(src, "html.parser")
results = soup.find( class_ = "ads ads--liquid ads--liquid--cols1to2")
results_list = soup.find_all("div", class_ = "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")
counter = 0
for add in results_list:
    time.sleep(2)
    counter += 1
    print(counter)
    add_id = add["data-entity-urn"].split(":")[3]
    object = add.find("a", class_ = "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
    add_url = object["href"]
    title = object.find("span").get_text().strip()
    print(title)
    add_content = lf.get_add_content(add_url)
    add_info = add_content[0]
    print(add_info)
    add_key_words = add_content[1]
    add_html_string = add_content[2]
    record = pd.DataFrame([[add_id, title, add_url, add_info, add_key_words, add_html_string]], columns=['ID','job_title','url','info', 'key_words', 'html_string'])
    df = pd.concat([df,record], axis = 0, ignore_index = True)
    
print("Number of adds extracted: " + str(df.shape[0]))

df.to_json(filepath, orient='records')
