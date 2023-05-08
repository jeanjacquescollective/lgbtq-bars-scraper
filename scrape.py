from itertools import zip_longest
from itertools import chain
import re
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from main import driver
import csv
import json









# get meta data from url
def getMetaDataFromUrl(driver, url):
    print('url' + url)
    latitude = re.search("!3d([0-9a-zA-Z.]+)!?", url).group(1)
    longitude = re.search("!4d([0-9a-zA-Z.]+)!?", url).group(1)
    title = driver.title.split(' - ')[0]
    metaData = {
        'coordinates': {
            'latitude': latitude,
            'longitude': longitude
        },
        'title': title,
        'url': url	
    }
    return metaData

def scrapeWebsite(driver, url):
    scrapedData = {}
    driver.get(url)
		# wait for elements of rush hours to load
		# these are the bars of the rush hour table
    WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.CLASS_NAME,"Liguzb"))
    
    chartBars = driver.find_elements(By.XPATH,"//img[contains(@src, 'lgbtq')]")
    title = driver.title.replace(' - Google Maps', '')
    scrapedData['metaData'] = getMetaDataFromUrl(driver,url)
    scrapedData['metaData'].update({
           'scrapedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           'address': driver.find_element(By.CLASS_NAME,"Io6YTe").text})
    # scrapedData['metaData'].update(getMetaDataFromUrl(driver,url))
    # scrapedData['metaData'].update({
		# 		'scrapedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'address': driver.find_element(By.CLASS_NAME,"Io6YTe").text,
		# })
    if(len(chartBars) > 0):
      scrapedData['lgtbq'] = True
    else:
      scrapedData['lgtbq'] = 'no'
    return title, scrapedData
        
    
    


def getLinks(driver, query, amount = 100):
    sites = []
    url = 'https://www.google.com/maps/search/' + query + '/'
    driver.get(url)
    t_end = time.time() + 3 * 1
    while len(driver.find_elements(By.CLASS_NAME,"hfpxzc")) < amount and time.time() < t_end:
        try:
            element = WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.XPATH,"(//a[@class='hfpxzc'])[last()]"))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            # print(e)
            pass
    links = driver.find_elements(By.CLASS_NAME,"hfpxzc")
    for link in links:    
        sites.append(link.get_attribute('href'))
    # print(len(sites))
    return sites
        
def scrapeDataFromLinks(driver, links, amount = 1):
		totalData = {}
		for link in links[:amount]:
			try:
					title, data = scrapeWebsite(driver, link)
					print('title' + title)
					totalData[''+title] = data
					print('Done with ' + title)
			except Exception as e:
					print(e )
					pass
		# driver.close() 
		return totalData


def main(driver, query, amount = 1):
	links = getLinks(driver, query, amount)
	data = scrapeDataFromLinks(driver, links, amount)
	# writeJson(data)
	print(data)
	return data
