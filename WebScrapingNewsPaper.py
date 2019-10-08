#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import os
import time
os.chdir('D:\\Google Drive\\HKU\\Year 4 Sem 1\\FINA4350 Text Analytics adn NLP in Finance')

from selenium import webdriver
import requests
from bs4 import BeautifulSoup as soup


# In[2]:


# # create function to extract news site
# def getNews(Newsurl):
#     browser.get(Newsurl)
#     time.sleep(5)
#     elem = browser.find_element_by_xpath("//*")
#     newspage = elem.get_attribute("outerHTML")
#     newspage_soup = soup(newspage)
#     opinionurl = newspage_soup.find("a", {"class":"pillar-link pillar-link--Opinion"})["href"]
#     browser.get(opinionurl)
#     time.sleep(5)
#     elem = browser.find_element_by_xpath("//*")
#     opinionspage = elem.get_attribute("outerHTML")
#     opinionspage_soup = soup(opinionspage)
#     for i in range(0,10):
#         opinion_title = opinionspage_soup.findAll("a", {"class":"fc-item__link"})[i]["href"]
#         opinion_link = opinionspage_soup.findAll("a", {"class":"fc-item__link"})[i]["href"]
#         browser.get(opinion_link)
#         time.sleep(5)
#         elem = browser.find_element_by_xpath("//*")
#         opinionpage = elem.get_attribute("outerHTML")
#         opinionpage_soup = soup(opinionpage)
#         para = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")]
#         # ! clean para1 and para2
#         opinion_text = para[1].text.replace("\n", " ") + " " +para[2].text.replace("\n", " ")
#         writecontent = opinion_title + "\t" + "\n"
#         f.write(writecontent)

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
            text = para1.replace("\ufffd", " ") + " " + para2.replace("\ufffd", " ")

            writetext = Date + "\t" + title + "\t" + text +"\n"

            f.write(writetext)

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
filename = "gardianpastopinion.tsv"
f = open(filename, "w")
headers = "Date\ttitle\ttext\n"
f.write(headers)

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
# close the tsv
f.close()



# In[6]:


# browser.get(sitelink)
# time.sleep(5)
# elem = browser.find_element_by_xpath("//*")
# opinionspage = elem.get_attribute("outerHTML")
# opinionspage_soup = soup(opinionspage)
# opinionlinks = [html["href"] for html in opinionspage_soup.findAll("a", {"class":"u-faux-block-link__overlay js-headline-text"})[0:10]]



# In[7]:


# opinionlinks = [html["href"] for html in opinionspage_soup.findAll("a", {"class":"u-faux-block-link__overlay js-headline-text"})[0:10]]


# In[8]:


# browser.get(opinionlinks[0])
# time.sleep(5)
# elem = browser.find_element_by_xpath("//*")
# opinionpage = elem.get_attribute("outerHTML")
# opinionpage_soup = soup(opinionpage)


# In[9]:


# elem = browser.find_element_by_xpath("//*")
# opinionpage = elem.get_attribute("outerHTML")
# opinionpage_soup = soup(opinionpage)
# para1 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[0].text
# para2 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[1].text


# In[10]:


# opinionpage_soup.find("h1").text.strip()


# In[11]:


# filename = "test.tsv"
# f = open(filename, "w")
# f.write("title\ttext\n")

# getNews(sitelink)

# f.close()


# In[12]:


# browser.get(link)
# time.sleep(5)
# elem = browser.find_element_by_xpath("//*")
# opinionpage = elem.get_attribute("outerHTML")
# opinionpage_soup = soup(opinionpage)
# title = opinionpage_soup.find("h1").text.strip()
# para1 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[0].text
# para2 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[1].text
# text = para1 + " " + para2


# In[13]:


# browser.get(sitelink)
# time.sleep(5)
# elem = browser.find_element_by_xpath("//*")
# opinionspage = elem.get_attribute("outerHTML")
# opinionspage_soup = soup(opinionspage)
# opinionlinks = [html["href"] for html in opinionspage_soup.findAll("a", {"class":"u-faux-block-link__overlay js-headline-text"})[0:10]]


# In[14]:


# browser.get(opinionlinks[6])
# elem = browser.find_element_by_xpath("//*")
# opinionpage = elem.get_attribute("outerHTML")
# opinionpage_soup = soup(opinionpage)


# In[15]:


# title = opinionpage_soup.find("h1").text.strip()
# para1 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[0].text
# para2 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[1].text
# text = para1 + " " + para2
# text


# In[16]:


#  title = opinionpage_soup.find("h1").text.strip()
# para1 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[0].text
# para2 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[1].text
# text = para1.replace("\ufffd", " ") + " " + para2.replace("\ufffd", " ")

# writetext = title + "\t" + text +"\n"


# In[17]:


# f.write(writetext)


# In[18]:


# f.close()
