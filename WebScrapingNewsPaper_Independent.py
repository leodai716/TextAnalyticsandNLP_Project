# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# In[1]:


# import libraries
import os
import time
os.chdir(r"D:\Google Drive\HKU\Year 4 Sem 1\FINA4350 Text Analytics adn NLP in Finance")

from selenium import webdriver
import requests
from bs4 import BeautifulSoup as soup


# In[2]:


def getNews(Newsurl):
    browser.get(Newsurl)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionspage = elem.get_attribute("outerHTML")
    opinionspage_soup = soup(opinionspage, features="lxml")
    opinionlinks = [divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"content premium-bg"})[0:2]] \
    +[divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"article type-article article-voices media-image"})[0:4]] \
    +[divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"article type-article article-voices media-video"})[0:4]]
    
    for link in opinionlinks:
        link = link[link.find('https'):]
        browser.get(link)
        time.sleep(5)
        elem = browser.find_element_by_xpath("//*")
        opinionpage = elem.get_attribute("outerHTML")
        opinionpage_soup = soup(opinionpage, features="lxml")
        title = opinionpage_soup.find("h1").text.strip().replace("\n", " ").replace("\u200b", " ").replace("\u200a", " ")
        fillloop1 = 0
        for fillloop in range(10):
            para1 = opinionpage_soup.find("div", {"class":"body-content"}).findAll("p")[fillloop].text.replace("\n", " ").replace("\u200b", " ").replace("\u200a", " ")
            if para1 != " ":
                fillloop1 = fillloop
                break
        for fillloop in range(1,10):
            para2 = opinionpage_soup.find("div", {"class":"body-content"}).findAll("p")[fillloop1+fillloop].text.replace("\n", " ").replace("\u200b", " ").replace("\u200a", " ")
            if para2 != " ":
                break
        text = para1.replace("\ufffd", " ") + " " + para2.replace("\ufffd", " ")
    
        writetext = Date + "\t" + title + "\t" + text +"\n"
        
        try:
            f = open(filename, "a", encoding= "utf-8")
            f.write(writetext)
            f.close() 
        except:
            continue



# In[3]:


# open firefox
#  *not use request because need to give time for the html to fully load
# executable_path points to the driver location, please download the driver before hand
browser = webdriver.Chrome(executable_path=r"D:\Python\Browser Drivers\chromedriver.exe")
# open website
browser.get('https://web.archive.org/web/*/https://www.independent.co.uk/voices')
# allow time for the website to full load the html
time.sleep(8)
# get html
elem = browser.find_element_by_xpath("//*")
# check for error
page = elem.get_attribute("outerHTML")
# res = requests.get(r'https://web.archive.org/web/*/https://www.theguardian.com')
# errorcheck = res.raise_for_status()


# In[4]:


# soup html parsing
page_soup = soup(page, features="lxml")
# find all the months
months = page_soup.findAll("div", {"class":"month"})


# In[5]:


# create tsv with headers
filename = "independentpastopinion.tsv"
f = open(filename, "w")
headers = "Date\ttitle\ttext\n"
f.write(headers)
f.close()


# loop through months
for month in months:
    month_title = month.div.text
    days = month.findAll("div", {"class":"calendar-day"})
    # check for days lenght
    if len(days) > 0:
        # loop through days
        for day in days:
            # get date
            date_title = str(day.find("a").text)
            Date = month_title + date_title
            # get site link
            sitelink = day.find("a")["href"]
            sitelink = "https://web.archive.org/" + sitelink
            getNews(sitelink)
