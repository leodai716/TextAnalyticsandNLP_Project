#!/usr/bin/env python
# coding: utf-8

# In[1]:

# import libraries
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup

#directory/URL setup:
extention_dir_str = r"C:\Users\marzl\Documents\#Python codes\#Browser Drivers\bypass-paywalls-chrome.crx"
webdriver_dir_str = r"C:\Users\marzl\Documents\#Python codes\#Browser Drivers\chromedriver.exe"
os.chdir('D:\\Google Drive\\HKU\\Year 4 Sem 1\\FINA4350 Text Analytics adn NLP in Finance')
filename = "telegraphpastopinion.tsv"
waybackMachineURL = 'https://web.archive.org/web/*/https://www.telegraph.co.uk/opinion/'

# In[2]:

#Telegraph changed layout twice. One starting from MAY29, and one from JUN20.
#This function is to distinguish between the layouts by their html contents
def layoutVersion(soup):
    if len(soup.find_all("a", {"class":"card__link u-clickable-area__link"})) > 0:
        return 1    #after MAY29
    elif len(soup.find_all("a", {"class":"list-headline__link u-clickable-area__link"})) > 0:
        return 2    #after JUN20
    else:
        return 0    #The oldest one

def getNews(Newsurl):
    browser.get(Newsurl)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionspage = elem.get_attribute("outerHTML")
    opinionspage_soup = soup(opinionspage, features="lxml")
    
    #See above: def layoutVersion(soup)
    if layoutVersion(opinionspage_soup) == 0:
        opinionlinks_raw = [h3Tag.a["href"] for h3Tag in opinionspage_soup.find_all(\
                            "h3")[0:10]]
    elif layoutVersion(opinionspage_soup) == 1:
        opinionlinks_raw = [aTag["href"] for aTag in opinionspage_soup.find_all(\
                            "a", {"class":"card__link u-clickable-area__link"})[0:10]]
    elif layoutVersion(opinionspage_soup) == 2:
        opinionlinks_raw = [aTag["href"] for aTag in opinionspage_soup.find_all(\
                            "a", {"class":"list-headline__link u-clickable-area__link"})[0:10]]

    #Extracting the original URL to read from, in order for Paywall Bypass to work
    opinionlinks = []    
    for link in opinionlinks_raw:
        opinionlinks.append(link[link.find("http"):])

    #Reading individual article:
    for link in opinionlinks:
        try:
            browser.get(link)
            time.sleep(5)
            elem = browser.find_element_by_xpath("//*")
            opinionpage = elem.get_attribute("outerHTML")
            opinionpage_soup = soup(opinionpage, features="lxml")
            title = opinionpage_soup.find("h1").text.strip()
            para1 = opinionpage_soup.find("div", {"class":"article__content js-article"}).find_all("p")[0].text
            para2 = opinionpage_soup.find("div", {"class":"article__content js-article"}).find_all("p")[1].text
            text = para1 + " " + para2
            #text = para1.replace("\ufffd", " ") + " " + para2.replace("\ufffd", " ") 
            #^^^(I don't see this line's necessity if I am just gonna utf-8-encode the file. Go ahead and decomment it if I'm mistakened)
            writetext = Date + "\t" + title + "\t" + text +"\n"
            
            f = open(filename, "a", encoding = "utf-8")
            f.write(writetext)
            f.close()
        except:
            continue
        
# In[3]:
        
#Option to run Paywall Bypass
options = webdriver.ChromeOptions()
options.add_extension(extention_dir_str)
# open Chrome with Paywall Bypass installed
browser = webdriver.Chrome(executable_path=webdriver_dir_str, options = options)
# open website
browser.get(waybackMachineURL)
# allow time for the website to full load the html
time.sleep(15)
# get html
elem = browser.find_element_by_xpath("//*")
page = elem.get_attribute("outerHTML")

# In[4]:

# soup html parsing
page_soup = soup(page, features="lxml")
# find all the months
months = page_soup.findAll("div", {"class":"month"})

# In[5]:

# create tsv with headers
f = open(filename, "a", encoding = "utf-8")
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