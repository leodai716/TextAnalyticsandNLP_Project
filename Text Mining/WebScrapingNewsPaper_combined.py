# -*- coding: utf-8 -*-
'''
This is a combined script for scraping news opinion
This script is written because of variation in data structure format and 
structure in previously scraped data
This script also hope to clean up some clutter found previously
Please do not run this code directly with cmd, until multiprocessing modlue has 
been added, else the programme would take days to complete
and is very suscpetible to errors
'''
#%% Init
import os
import sys
# scraping
import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup
# storing data
import re
import numpy as np
import pandas as pd
# multiprocessing
import multiprocessing

sys.path.append('../')
import _LocalVariable

#%% multiprocessing
cores_allocated = int(multiprocessing.cpu_count()/2-1)

#%% source
guardian_website = 'https://web.archive.org/web/*/https://www.theguardian.com/uk/commentisfree'
express_website = 'https://web.archive.org/web/*/https://www.express.co.uk/comment'
independent_website = 'https://web.archive.org/web/*/https://www.independent.co.uk/voices'
sources = [guardian_website, express_website, independent_website]
news_papers = ['guardian', 'express', 'independent']
#%% common function
def get_opinion(website, func):
    # create empty dataframe
    data = pd.DataFrame(columns=np.array(['Date','title','text']))

    # open browser
    browser_options = webdriver.ChromeOptions()
    browser_options.add_extension(_LocalVariable._BYPASS_FIREWALL_CHROME_PATH)
    browser = webdriver.Chrome(executable_path=_LocalVariable._CHROME_DRIVER_PATH,\
                               options=browser_options)

    # open website
    browser.get(website)
    time.sleep(5)
    # get html
    elem = browser.find_element_by_xpath("//*")
    page = elem.get_attribute("outerHTML")
    # parsing
    page_soup = soup(page, features="lxml")
    months_html = page_soup.findAll("div", {"class":"month"})

    # get data
    for month_html in months_html:
        month_title = month_html.div.text
        days_html = month_html.findAll("div", {"class":"calendar-day"})
        
        if len(days_html) > 0:
            for day_html in days_html:
                # get date
                date_title = str(day_html.find("a").text)
                Date = month_title + date_title
                
                # get site link
                sitelink = day_html.find("a")["href"]
                sitelink = "https://web.archive.org/" + sitelink
                func(sitelink,browser,data,Date)
    return data
            
    
#%% page specific functions 

def get_guardian(Newsurl,browser,data,Date):
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
            para3 = opinionpage_soup.find("div", {"class":"content__article-body from-content-api js-article__body"}).findAll("p")[2].text
            text = re.sub("[^a-zA-Z]+", " ", para1 ) + " " + re.sub("[^a-zA-Z]+", " ", para2) + " " + re.sub("[^a-zA-Z]+", " ", para3 )
            
            temp_data = pd.DataFrame(np.array([Date,title,text]))
            temp_data = temp_data.T
            temp_data.columns = np.array(['Date','title','text'])
            
            
            data = pd.concat([data, temp_data], ignore_index=True)
        except:
            pass
    return data

def get_express(Newsurl,browser,data,Date):
    browser.get(Newsurl)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionpage = elem.get_attribute("outerHTML")
    opinionpage_soup = soup(opinionpage, features="lxml")
    # find links for each opinion
    opiniontags = opinionpage_soup.findAll("div", {"class":"lazy-container"})
    opiniontags = opiniontags[0:10]
    opinionlinks = [tag.parent["href"][1:] for tag in opiniontags]
    opinionlinks = ["https://web.archive.org" + link for link in opinionlinks]
    for link in opinionlinks:
        try:
            browser.get(link)
            time.sleep(5)
            elem = browser.find_element_by_xpath("//*")
            opinion = elem.get_attribute("outerHTML")
            opinion_soup = soup(opinion, features="lxml")
            title = opinion_soup.find("div", {"id":"singleArticle"}).find("h1").text.strip()
            para1 = opinion_soup.find("div", {"id":"singleArticle"}).find("h3").text
            para2 = opinion_soup.find("div", {"id":"singleArticle"}).findAll("p")[0].text+" "+ opinion_soup.find("div", {"id":"singleArticle"}).findAll("p")[1].text
    
            text = re.sub("[^a-zA-Z]+", " ", para1 ) + " " + re.sub("[^a-zA-Z]+", " ", para2)
    
            temp_data = pd.DataFrame(np.array([Date,title,text]))
            temp_data = temp_data.T
            temp_data.columns = np.array(['Date','title','text'])
            
            
            data = pd.concat([data, temp_data], ignore_index=True)
        except:
            pass
    return data


def get_independent(Newsurl,browser,data,Date):
    browser.get(Newsurl)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionspage = elem.get_attribute("outerHTML")
    opinionspage_soup = soup(opinionspage, features="lxml")
    opinionlinks = [divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"content premium-bg"})[0:2]] \
    +[divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"article type-article article-voices media-image"})[0:4]] \
    +[divTag.a["href"] for divTag in opinionspage_soup.find_all("div", {"class":"article type-article article-voices media-video"})[0:4]]
    
    for link in opinionlinks:
        try:
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
            text = re.sub("[^a-zA-Z]+", " ", para1 ) + " " + re.sub("[^a-zA-Z]+", " ", para2 )
            temp_data = pd.DataFrame(np.array([Date,title,text]))
            temp_data = temp_data.T
            temp_data.columns = np.array(['Date','title','text'])
            
            data = pd.concat([data, temp_data], ignore_index=True)
        except:
            pass
    return data
functions = [get_guardian, get_express, get_independent]
#%% Main

def call_func(i):
    data = get_opinion(sources[i], functions[i])
    data['news_paper'] = news_papers[i]
    return data

data = call_func(1)
#if __name__ == '__main__':
#    with multiprocessing.Pool(processes=cores_allocated) as pool:
#        results = pool.map(call_func,\
#                          range(len(sources)))
#        
#        data = pd.concat(results, ignore_index=True)

        
    