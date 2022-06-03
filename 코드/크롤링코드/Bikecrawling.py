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

search = input('검색어:')
browser = input('브라우저(1: 크롬, 2: 엣지): ')

url=f'https://duckduckgo.com/?q={search}&t=h_&iax=images&ia=images'
driver = webdriver.Edge() if browser == '2' else webdriver.Chrome()
driver.get(url)

# scroll to max search length
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(SCROLL_PAUSE_TIME) 
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
imgs = soup.select('img.tile--img__img')
print(len(imgs))

dir = ".\\"+search
imgurls= []
createDirectory(dir)
for img in imgs:
    try:
        src = img.attrs["src"]
        imgurls.append("https:" + src)
    except KeyError:
        src = img.attrs["data-src"]
        imgurls.append("https:" + src)

n = 1
for imgurl in imgurls:
    path = os.path.dirname(os.path.abspath(__file__))+dir.strip(".")+"\\"
    fname = f"{path + search + str(n)}.png"
    #print(fname)
    urlretrieve(imgurl, fname)
    n += 1

driver.quit()
