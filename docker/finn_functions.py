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

    #Dives into last changed part
    soup_last_changed = BeautifulSoup(page.content, "html.parser").find_all("tr")
    for element in soup_last_changed:
        if re.search('Sist endret', element.get_text()):
            last_changed = element.find("td").get_text()
            last_changed = dateparser.parse(last_changed,settings={'TIMEZONE': 'CET'}).strftime("%Y-%m-%d %H:%M")
    #print(last_changed)

    #Dives into main part
    soup = soup.body.main.find("div", {"data-owner" : "adView"}).find(lambda tag: tag.name == 'div' and tag.get('class') == ['grid'])
    soup = soup.find("div", class_ = "grid__unit u-r-size2of3").find("div", class_ = "u-word-break").find_all("section", class_ = "panel")

    #Extracts section 2 info
    info = soup.pop(1) 
    info_header = info.find_all("dt")
    info_header_content =  [item.contents[0] for item in info_header]
    info_description = info.find_all("dd")
    info_description_content = [item.contents[0] for item in info_description]
    #Converts date format if date. If string, does nothing.
    info_description_content[2] =  check_and_convert_date(info_description_content[2])
    info = {info_header_content[i]: info_description_content[i] for i in range(len(info_header_content))}
    #print(info)

    # Extract keywords and add remaining text to html_string
    html_string = ""
    key_words = ""
    for section in soup :
        if re.search("Nøkkelord", section.get_text()) :
            key_words = section.find("p").text.strip()
            #print(key_words)
        else :
            html_string += section.text
            #print(html_string)


    return info, last_changed, key_words, html_string

#Azure data lake
def upload_file_to_directory(file, filename):
    from azure.storage.filedatalake import DataLakeServiceClient
    try:

        file_system_client = service_client.get_file_system_client(file_system="jobads")

        directory_client = file_system_client.get_directory_client("finn_jobs")
        
        file_client = directory_client.create_file(filename)

        file_contents = file

        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))

        file_client.flush_data(len(file_contents))

    except Exception as e:
      print(e)

def initialize_storage_account():
    from azure.storage.filedatalake import DataLakeServiceClient
    storage_account_name = "lake4jobadd"
    storage_account_key = "ZRZVJ/YJu0L1ueRnAaacpHMRqCB4feT+w6hR9xhYxCRe1/Y1Iqd2Tn/IJzbVqFKRHqx5rRjbvGssWPFw0Ims6g=="
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)