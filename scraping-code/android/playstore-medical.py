#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("window-size=1200x600")


driver = webdriver.Chrome("/Users/yusufsaheed/Downloads/chromedriver", chrome_options=options)

CATEGORIES = [None, "ct|apps_topselling_paid", "ct|apps_topgrossing"]
MEDICAL_URL = 'https://play.google.com/store/apps/category/MEDICAL'

COUNTRY_CODES = ['HR', 'CY', 'CZ', 'DK', 'EE', 'FO', 'FI', 'FR', 'GF', 'PF', 'DE', 'GI', 'GR', 'GL', 'GP', 'HU', 'IS', 'IE', 'IT', 'LV', 'LI', 
                'LT', 'LU', 'MT', 'MQ', 'YT', 'MC', 'NL', 'NC', 'NO', 'PL', 'PT', 'RE', 'RO', 'SM', 'SK', 'SI', 'ES', 'BL', 'MF', 'PM', 'SJ', 
                'SE', 'GB', 'VA', 'WF', 'AX', 'AT', 'BE', 'BG']


def get_all_links_from_page(baseurl, idClicks):
    links_set = set()
    for idClick in idClicks:
        driver = webdriver.Chrome("/Users/yusufsaheed/Downloads/chromedriver", chrome_options=options)
        driver.get(baseurl)
        if idClick != None:
            more_button = driver.find_element(by=By.ID, value=idClick)
            more_button.click()
            time.sleep(2)
        gp_links = driver.find_elements(By.CLASS_NAME, value='VfPpkd-WsjYwc')
        for j in gp_links:
            links_set.add(j.find_element(by=By.TAG_NAME, value='a').get_attribute('href'))
    return links_set

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


for country_code in COUNTRY_CODES:
    is_done = False
    while(is_done == False):
        try:
            with (open(f'google-medical-{country_code}.csv', 'w+')) as new_file:
                keys = ['App Name', 'Age Rating', 'Price', 'InApp Purchase', 'Average Rating', 'Rating Count',
                    'App Link', 'Last Updated', 'Released Date', 'Downloads', 'Version', 'Country Code']
                mywriter = csv.DictWriter(new_file, keys)
                mywriter.writeheader()
                links = get_all_links_from_page(f'{MEDICAL_URL}?gl={country_code}', CATEGORIES)
                for link in links:
                    val = processInformation(link)
                    val['Country Code'] = country_code
                    mywriter.writerow(val)
            is_done = True
        except:
            print(f"Retrying {country_code} due to error")



