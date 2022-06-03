from urllib.request import  urlopen
from urllib.request import  urlretrieve
from urllib.parse import  quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
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
url=f'https://www.google.co.kr/imghp?hl=ko&tab=ri&ogbl&q={quote_plus(search)}'
driver = webdriver.Chrome()
driver.get(url)

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
img = soup.select('.rg_i.Q4LuWd')
n=1
imgurl= []

dir = ".\\"+search
createDirectory(dir)
for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])

for i in imgurl:
    path = os.path.dirname(os.path.abspath(__file__))+dir.strip(".")+"\\"
    urlretrieve(i,path+search+str(n)+".jpg")
    n+=1
    if(n>10):
        break

driver.close()
