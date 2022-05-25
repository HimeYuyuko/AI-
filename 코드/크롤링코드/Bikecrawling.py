from urllib.request import  urlopen
from urllib.request import  urlretrieve
from urllib.parse import  quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

search = input('검색어:')
url=f'https://www.google.com/search?q={quote_plus(search)}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjT-bLHvPr3AhVJx2EKHQU9A-0Q_AUoAXoECAIQAw&biw=929&bih=874&dpr=1'
driver = webdriver.Chrome()
driver.get(url)
for i in range(500):
    driver.execute_script("window.scrollBy(0,100000)")

html = driver.page_source
soup = BeautifulSoup(html)
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
    path = "C:\\Users\\sky15\\PycharmProjects\\pythonProject2"+dir.strip(".")+"\\"
    urlretrieve(i,path+search+str(n)+".jpg")
    n+=1
    if(n>10):
        break
driver.close()