#Module containing functions relevant for finn.no adds

#Check and converts date 
def check_and_convert_date(date):
    import re
    import dateparser
    from datetime import datetime
    pattern = re.compile("^[0-9]{2}.[0-9]{2}.[0-9]{4}$")
    if pattern.match(date):
        date = date + " 23:59"
        date_pased = datetime.strptime(date, "%d.%m.%Y %H:%M" ).strftime("%Y-%m-%d %H:%M")
        return date_pased
    else:
        return date

#Extracts add contents and returns as tuple
def get_add_content(add_url):
    import requests
    import re
    from datetime import datetime
    from bs4 import BeautifulSoup
    import dateparser 

    URL = add_url
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    #Dives into header
    soup_header = BeautifulSoup(page.content, "html.parser").find("h4", class_ = "top-card-layout__second-subline")
    header = {}
    header['company'] = soup_header.find_all(class_ = "topcard__flavor-row")[0].find("a").contents[0].strip()

    header['location'] = soup_header.find_all(class_ = "topcard__flavor-row")[0].find(class_ = "topcard__flavor topcard__flavor--bullet").contents[0].strip()

    header['posted_time_ago'] = soup_header.find("span", class_ = "posted-time-ago__text").contents[0].strip()

    header['num_applicants'] = soup_header.find(class_ = "num-applicants__caption").contents[0].strip()

    #Job criterias
    job_criterias = soup.find("ul", class_ = "description__job-criteria-list")

    job_criteria_headers = job_criterias.find_all("h3")
    job_criteria_headers = [criteria.contents[0].strip() for criteria in job_criteria_headers]

    job_criteria_descriptions = job_criterias.find_all("span")
    job_criteria_descriptions = [description.contents[0].strip() for description in job_criteria_descriptions]

    job_criteria_dict = dict(zip(job_criteria_headers,job_criteria_descriptions))

    #Main text
    main_text = soup.find("div", class_ = "description__text").find("section").find("div").get_text()

    return header, job_criteria_dict, main_text


def scroll_to_bottom(driver):
    from selenium import webdriver
    import time
    start = time.time()
  
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll 
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000
    
        # we will stop the script for 3 seconds so that 
        # the data can load
        time.sleep(1)
        # You can change it as per your needs and internet speed
    
        end = time.time()
    
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 20:
            break
