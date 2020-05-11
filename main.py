import requests
import extracter
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")


# app_id = input("Application id : ")
app_id = input("Enter application ID: ")
url = "https://play.google.com/store/apps/details?id=" + app_id + "&showAllReviews=true"

browser.get(url)
# U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 400

path1 = '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span'
path2 = '/html/body/div[1]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span'
path3 = '/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span'

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)

    if((no_of_pagedowns - 1) % 12 == 0):
        for path in [path1, path2, path3]:
            try:
                python_button = browser.find_elements_by_xpath(path)[0]
                python_button.click()
            except:
                elem.send_keys(Keys.PAGE_UP)
                pass
    if((no_of_pagedowns - 1) % 25 == 0):
        for path in [path1, path2, path3]:
            try:
                elem.send_keys(Keys.PAGE_UP)
                python_button = browser.find_elements_by_xpath(path)[0]
                python_button.click()
            except:
                pass
    no_of_pagedowns -= 1
    print(430 - no_of_pagedowns)


# Now that the page is fully scrolled, grab the source code.

print("STEP1")
source_data = browser.page_source
print("SETP2")
soup = BeautifulSoup(source_data, 'html.parser')

print("SETP3")
# Revirew main div
review_divs = soup.find("div", {"jsname": "fk8dgd"})
print("STEP4")
# Find each review div elements
reviews = review_divs.findAll("div", {"jscontroller": "H6eOGe"})

print("Gathering Reviews")
print("=============Reviews=============")
r = 0
# Iterate through each review
for div in reviews:
    r = r + 1
    print(r)
    user = div.find("span", {"class": "X43Kjb"})
    user = user.text.encode('unicode-escape').decode('utf-8')
    rating = div.find("div", {"class", "pf5lIe"})
    rating = rating.find("div", {"aria-label": re.compile('Rated')})
    rating = str(rating.get('aria-label'))
    rating = rating[6]
    review = div.find("span", {"jsname": "fbQN7e"})
    review = review.text.encode('unicode-escape').decode('utf-8')
    if(review == ""):
        print("Short Review")
        review = div.find("span", {"jsname": "bN97Pc"})
        review = review.text
    content = {'Sno': r, 'User': user, "Rating": rating, "Review": review}
    extracter.writecsv(app_id, content)
