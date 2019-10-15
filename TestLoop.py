month = months[0]
days = month.findAll("div", {"class":"calendar-day"})


day = days[0]
sitelink = day.find("a")["href"]
sitelink = "https://web.archive.org/" + sitelink

browser.get(sitelink)
time.sleep(5)
elem = browser.find_element_by_xpath("//*")
opinionspage = elem.get_attribute("outerHTML")
opinionspage_soup = soup(opinionspage, features="lxml")
opinionlinks = [html["href"] for html in opinionspage_soup.findAll("a", {"class":"u-faux-block-link__overlay js-headline-text"})[0:10]]

link = opinionlinks[0]
browser.get(link)
time.sleep(5)
elem = browser.find_element_by_xpath("//*")
opinionpage = elem.get_attribute("outerHTML")
opinionpage_soup = soup(opinionpage, features="lxml")
title = opinionpage_soup.find("h1").text.strip()
