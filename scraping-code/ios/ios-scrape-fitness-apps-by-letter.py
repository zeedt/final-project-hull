
import imp
from pendulum import time
import requests
from bs4 import BeautifulSoup
import csv
import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/yusufsaheed/Downloads/chromedriver", chrome_options=options)


base_urls = [{'url':'https://apps.apple.com/us/genre/ios-health-fitness/id6013', 'type' : 'fitness'}]
# letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
#           'U', 'V', 'W', 'X', 'Y', 'Z']

def processAppInformation(page_source, link=None):
    # print("Processing => ", link)
    # page = requests.get(link)
    soup = BeautifulSoup(page_source, "lxml")
    val = {'App Name' : 'N/A',
            'Size' : 'N/A',
            'Age Rating' : 'N/A',
            'Languages' : 'N/A',
            'Price' : 'N/A',
            'InApp Purchase' : 'N/A',
            'Average Rating' : 'N/A',
            'Rating Count'  : 'N/A',
            'Privacy Data' : 'N/A',
            'App Link' : link
          }
    appName = soup.find(class_="product-header__title app-header__title").text.strip()
    val['App Name'] = appName
    info_list = soup.findAll(class_="information-list__item l-column small-12 medium-6 large-4 small-valign-top")
    for info in info_list:
        dt_text =info.find("dt").text.strip()
        if (dt_text == 'Size'):
            val['Size'] = info.find("dd").text.strip()
        elif (dt_text == 'Age Rating'):
            val['Age Rating'] = info.find("dd").text.strip()
        elif (dt_text == 'Languages'):
            val['Languages'] = info.find("dd").text.strip()
        elif (dt_text == 'Price'):
            val['Price'] = info.find("dd").text.strip()
        elif (dt_text == 'In-App Purchases'):
            val['InApp Purchase'] = True
    average_rating = soup.find(class_="we-customer-ratings__averages__display")
    if (average_rating != None):
        val['Average Rating'] = average_rating.text.strip()
    
    rating_count = soup.find(class_="we-customer-ratings__count small-hide medium-show")
    if (rating_count != None):
        val['Rating Count'] = rating_count.text.strip()
    
    collected_data = soup.findAll(class_="privacy-type__grid-content privacy-type__data-category-heading")
    privacy_data = []
    for data in collected_data:
        privacy_data.append(data.text.strip())
    if (len(privacy_data) > 0):
        val['Privacy Data'] = ','.join(privacy_data)
    
    # print(val)
    return val



def get_all_links_from_page(baseurl, pageLetter, pageNo=1, links=[]):
    current_page = f"{baseurl}?letter={pageLetter}&page={pageNo}#page"
    # print("current page is " , current_page)
    letter_page = requests.get(current_page)
    soup = BeautifulSoup(letter_page.content, "html.parser")
    letter_page_results = soup.find(id="selectedcontent")
    links_in_page = letter_page_results.find_all("a")
    for link in links_in_page:
        links.append(link['href'])
    nextPages = soup.findAll(class_="paginate-more")
    if (len(nextPages) == 0):
        return links
    return get_all_links_from_page(baseurl,pageLetter,pageNo+1, links)


def execute_crawl(letters):
    for base_url in base_urls:
        for letter in letters:
            missed = 0
            start = time.time()
            app_type = base_url['type']
            keys = ['App Name', 'Size' , 'Age Rating','Languages', 'Price' ,'InApp Purchase', 'Average Rating',
                'Rating Count', 'Privacy Data', 'App Link', 'Number of Versions', 'Last Version Date', 'First Version Date' ]
            with (open(f'{app_type}-{letter}.csv', 'w+')) as new_file:
                mywriter = csv.DictWriter(new_file, keys)
                mywriter.writeheader()
                total_app_links = get_all_links_from_page(base_url['url'], letter)
                print(f"Total app links for {base_url} and letter {letter} =>{len(total_app_links)}")
                for link in total_app_links:
                    try:
                        driver.get(link)
                        val = processAppInformation(driver.page_source, link)
                        more_buttons = driver.find_elements_by_tag_name("button")
                        version_button = None
                        for button in more_buttons:
                            if (button.text == 'Version History'):
                                version_button = button
                                break
                        if (version_button != None):
                            driver.execute_script("arguments[0].click();", version_button)
                            page_source = driver.page_source
                            version_history = driver.find_elements_by_class_name("version-history__item")
                            val['Number of Versions'] = len(version_history)
                            soup = BeautifulSoup(page_source, "lxml")
                            version_dates = soup.findAll(class_='version-history__item__release-date')
                            val['Last Version Date'] = version_dates[0].text.strip()
                            val['First Version Date'] = version_dates[len(version_dates)-1].text.strip()
                        else:
                            val['First Version Date'] = 'N/A'
                            val['Last Version Date'] = 'N/A'
                            val['Number of Versions'] = '1'
                        mywriter.writerow(val)
                    except Exception as e:
                        missed = missed + 1
                        print("Unable to process app link ", link, " due to ", e)
                        print("Number missed ", missed)
            end = time.time()
            print(f"Took {end-start} seconds to process for page {base_url}")
            print("Missed => ", missed)
        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--letters",
        default="",
        help="tLetters separated with comma"
    )
    args = parser.parse_args()

    execute_crawl(args.letters.split(','))