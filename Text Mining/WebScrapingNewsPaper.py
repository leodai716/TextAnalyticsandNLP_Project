#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import os
import time
import sys

sys.path.append("../")

import _LocalVariable

os.chdir(_LocalVariable._DATA_DIRECTORY)
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as soup
import re


# In[2]:


def getNews(Newsurl):
    browser.get(Newsurl)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionspage = elem.get_attribute("outerHTML")
    opinionspage_soup = soup(opinionspage, features="lxml")
    opinionlinks = [html["href"] for html in opinionspage_soup.findAll("a", {"class":"u-faux-block-link__overlay js-headline-text"})[0:10]]
    for link in opinionlinks:
        try:
            browser.get(link)
            time.sleep(5)
            elem = browser.find_element_by_xpath("//*")
            opinionpage = elem.get_attribute("outerHTML")
            opinionpage_soup = soup(opinionpage, features="lxml")
            title = opinionpage_soup.find("h1").text.strip()
            para1 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[0].text
            para2 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[1].text
            text = re.sub("[^a-zA-Z]+", " ", para1 ) + " " + re.sub("[^a-zA-Z]+", " ", para2)

            writetext = Date + "\t" + title + "\t" + text +"\n"
            
            f = open(filename, "a")
            f.write(writetext)
            f.close()


        except:
            continue





# In[3]:


# open firefox
#  *not use request because need to give time for the html to fully load
# executable_path points to the driver location, please download the driver before hand
browser = webdriver.Firefox(executable_path=r"D:\Python\Browser Drivers\geckodriver.exe")
# open website
browser.get('https://web.archive.org/web/*/https://www.theguardian.com/uk/commentisfree')
# allow time for the website to full load the html
time.sleep(15)
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
filename = "raw_data-opinion-guadian-remove_nonalp.tsv"
f = open(filename, "w")
headers = "Date\ttitle\ttext\n"
f.write(headers)
f.close()


# loop through months
for month in months:
    try:
        month_title = month.div.text
        days = month.findAll("div", {"class":"calendar-day"})
        # check for days lenght
        if len(days) > 0:
            # loop through days
            for day in days:
                try:
                    # get date
                    date_title = str(day.find("a").text)
                    Date = month_title + date_title
                    # get site link
                    sitelink = day.find("a")["href"]
                    sitelink = "https://web.archive.org/" + sitelink
                    getNews(sitelink)
                except:
                    continue
    except:
        continue




