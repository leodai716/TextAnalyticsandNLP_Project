# This is a code scripted for getting the comments on Express.com

#%% Define Variables
# load local parameters
exec(open("../LocalParameter.py").read())

filename = "expressopinion.tsv"
news_website_link = 'https://web.archive.org/web/*/https://www.express.co.uk/comment'

#%% Init
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup as soup

os.chdir("../")

#%% Functions

# get opinion links
def get_opinion_links(opinionpagelink):
    browser.get(opinionpagelink)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinionpage = elem.get_attribute("outerHTML")
    opinionpage_soup = soup(opinionpage, features="lxml")
    # find links for each opinion
    opiniontags = opinionpage_soup.findAll("div", {"class":"lazy-container"})
    opiniontags = opiniontags[0:10]
    opinionlinks = [tag.parent["href"][1:] for tag in opiniontags]
    opinionlinks = ["https://web.archive.org" + link for link in opinionlinks]

    return opinionlinks

# get opinion content
def get_opinion_content(opinionlink):
    browser.get(opinionlink)
    time.sleep(5)
    elem = browser.find_element_by_xpath("//*")
    opinion = elem.get_attribute("outerHTML")
    opinion_soup = soup(opinion, features="lxml")
    title = opinion_soup.find("div", {"id":"singleArticle"}).find("h1").text.strip()
    para1 = opinion_soup.find("div", {"id":"singleArticle"}).find("h3").text
    para2 = opinion_soup.find("div", {"id":"singleArticle"}).findAll("p")[0].text+" "+ opinion_soup.find("div", {"id":"singleArticle"}).findAll("p")[1].text
    text = para1.replace("\ufffd", " ") + " " + para2.replace("\ufffd", " ")
    content = Date + "\t" + title + "\t" + text +"\n"

    return content

#%% Text mining from express.co.uk/comment

browser = webdriver.Firefox(executable_path = firefox_driver_path)

# create empty tsv with headers
f = open(filename, "w")
headers = "Date\ttitle\ttext\n"
f.write(headers)
f.close()


# to to internet archive
browser.get(news_website_link)
time.sleep(5)

# get and parse html
elem = browser.find_element_by_xpath("//*")
page = elem.get_attribute("outerHTML")
page_soup = soup(page, features="lxml")

# find all the months
months = page_soup.findAll("div", {"class":"month"})

# loop through months
for month in months:
    try:
        month_title = month.div.text
        days = month.findAll("div", {"class":"calendar-day"})
        # check for days lengh
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

                    # get opinion
                    opinionlinks = get_opinion_links(sitelink)

                    for link in opinionlinks:
                        content = get_opinion_content(link)

                        # write to file

                        f = open(filename, "a")
                        print(content)
                        f.write(content)
                        f.close()
                except:
                    continue
    except:
        continue
