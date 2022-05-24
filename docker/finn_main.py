from ast import Break
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import re
import dateparser
import finn_functions as ff
import time

extraction_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
filename = r'finn_jobs_' + extraction_time + '.json'
print(filename)

URL = "https://www.finn.no/job/fulltime/search.html?abTestKey=control&q=%22data+engineer%22&sort=RELEVANCE"
page = requests.get(URL)
df = pd.DataFrame({'ID':[],'extraction_time':[], 'last_changed':[], 'job_title':[],'url':[], 'info':[],  'key_words':[], 'html_string':[]})

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find( class_ = "ads ads--liquid ads--liquid--cols1to2")
results_list = results.find_all("article", class_ = "ads__unit")
counter = 0
for add in results_list:
    time.sleep(1)
    object = add.find("div", class_ = "ads__unit__content")
    
    #Check if add is promoted. If so, skip to not duplicate.
    check = re.search('Betalt plassering',str(object))
    if check:
        continue
    title_url_object = object.find("h2").find("a")
    title = title_url_object.contents[0]
    print(title)
    add_url = title_url_object["href"]
    add_id = title_url_object["id"]
    #print(extraction_time)
    add_content = ff.get_add_content(add_url)
    add_info = add_content[0]
    add_last_changed = add_content[1]
    #print(add_last_changed)
    add_key_words = add_content[2]
    add_html_string = add_content[3]
    record = pd.DataFrame([[add_id, extraction_time, add_last_changed, title, add_url, add_info, add_key_words, add_html_string]], columns=['ID','extraction_time','last_changed','job_title','url','info', 'key_words', 'html_string'])
    df = pd.concat([df,record], axis = 0, ignore_index = True)
    counter += 1
    
#print("Number of adds extracted: " + str(df.shape[0]))

file = df.to_json(orient='records',indent = 2)

ff.initialize_storage_account()
ff.upload_file_to_directory(file, filename)




