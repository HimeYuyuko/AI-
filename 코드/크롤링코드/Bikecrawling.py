from urllib.request import  urlopen, urlretrieve
from urllib.parse import  quote_plus

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os
import time

SCROLL_PAUSE_TIME = 1

def createDirectory(directory):
    '''just create directory'''
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

url=f'https://www.google.co.kr/imghp?hl=ko&tab=ri&ogbl'
search = input('검색어:')
browser = input('브라우저(1: 크롬, 2: 엣지): ')

driver = webdriver.Edge() if browser == '2' else webdriver.Chrome()
driver.get(url)

elem = driver.find_element(By.NAME, 'q')
elem.send_keys(search)
elem.send_keys(Keys.RETURN)

# scroll to max search length
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(SCROLL_PAUSE_TIME) 
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        try:    
            driver.find_element_by_css_selector('.mye4qd').click()
        except:
            break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
imgs = soup.select('.rg_i.Q4LuWd')

dir = ".\\"+search
imgurls= []
createDirectory(dir)
for img in imgs:
    try:
        imgurls.append(img.attrs["src"])
    except KeyError:
        imgurls.append(img.attrs["data-src"])

n=1
for imgurl in imgurls:
    path = os.path.dirname(os.path.abspath(__file__))+dir.strip(".")+"\\"
    urlretrieve(imgurl, path+search+str(n)+".jpg")
    n+=1

driver.close()
