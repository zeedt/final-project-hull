from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("window-size=1200x600")

driver = webdriver.Chrome("/Users/yusufsaheed/Downloads/chromedriver", chrome_options=options)

def get_all_links_from_page_file():
    links = []
    BASE_URL = 'https://play.google.com'
    with open('playstore-workout.html', 'r') as f:

        contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')
        link_elements = soup.find_all('a')
        for link in link_elements:
            links.append(f'{BASE_URL}{link["href"]}')
    return links


def processInformation(link):
    val = {'App Name' : 'N/A',
        'Age Rating' : 'N/A',
        'Price' : 'N/A',
        'InApp Purchase' : 'N/A',
        'Average Rating' : 'N/A',
        'Rating Count'  : 'N/A',
        'App Link' : link,
        'Last Updated' : 'N/A',
        'Released Date' : 'N/A',
        'Downloads' : 'N/A',
        'Version' : 'N/A'   
      }
    
    driver.get(link)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    review_page = soup.find_all(class_='P4w39d')
    
    if (len(review_page) > 0):
        val['Average Rating'] = review_page[0].find_all(class_='jILTFe')[0].text.strip()
        val['Rating Count'] = review_page[0].find_all(class_='EHUI5b')[0].text.strip().replace(' reviews', '')
    
    pay_button = soup.select('div > c-wiz > div > div > div > div > button > span > span > span > meta:nth-child(2)')

    if (len(pay_button) > 0):
        val['Price'] = pay_button[0]['content']
    
    more_buttons = driver.find_element_by_xpath(
        '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button')

    
    driver.execute_script("arguments[0].click();", more_buttons)
    soup = BeautifulSoup(driver.page_source, "lxml")
    letter_page_results = soup.find(id="yDmH0d")
    val['App Name'] = letter_page_results.find_all(class_='xzVNx')[0].text.strip()
    val['InApp Purchase'] = len(letter_page_results.find_all(class_='UIuSk')) > 0
    
    about_page = letter_page_results.find_all(class_="sMUprd")
    for info in about_page:
        dt_text =info.find_all(class_="q078ud")[0].text.strip()
        dt_val = info.find_all(class_="reAt0")[0].text.strip()
        
        if (dt_text == 'Content rating'):
            val['Age Rating'] = dt_val.replace('\xa0Learn more', '')
        elif (dt_text == 'Downloads'):
            val['Downloads'] = dt_val.replace('downloads', '')
        elif (dt_text == 'Released on'):
            val['Released Date'] = dt_val
        elif (dt_text == 'Updated on'):
            val['Last Updated'] = dt_val
        elif (dt_text == 'Version'):
            val['Version'] = dt_val
    return val

all_links = get_all_links_from_page_file()

with (open('google-playstore-workout.csv', 'w+')) as new_file:
    keys = ['App Name', 'Age Rating', 'Price', 'InApp Purchase', 'Average Rating', 'Rating Count',
        'App Link', 'Last Updated', 'Released Date', 'Downloads', 'Version']
    mywriter = csv.DictWriter(new_file, keys)
    mywriter.writeheader()
    for link in all_links:
        val = processInformation(link)
        mywriter.writerow(val)