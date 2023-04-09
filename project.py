import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re
from pymongo import MongoClient


def saveString(html, filename):
    try:
        file = open(filename, "w")
        file.write(str(html))
        file.close()
    except Exception as ex:
        print('Error: ' + str(ex))


def loadString(filename):
    try:
        html = open(filename, "r", encoding='utf-8').read()
        return (html)
    except Exception as ex:
        print('Error: ' + str(ex))

##################################################################################################################
################################## Question 2 ####################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

###############################Change Global Path Here!################################################################################
#######################################################################################################################################
driver = webdriver.Chrome(executable_path='/Users/jiayi/Downloads/chromedriver_mac_arm64/chromedriver')
#######################################################################################################################################
#######################################################################################################################################
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)
driver.get("https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold");

rank1_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/4873']")

rank1_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[1].htm")
driver.back()
time.sleep(5)


rank2_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/8861']")

rank2_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[2].htm")
driver.back()
time.sleep(5)


rank3_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/3105']")

rank3_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[3].htm")
driver.back()
time.sleep(5)

rank4_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/544']")

rank4_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[4].htm")
driver.back()
time.sleep(5)

rank5_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/811']")

rank5_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[5].htm")
driver.back()
time.sleep(5)

rank6_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/4580']")

rank6_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[6].htm")
driver.back()
time.sleep(5)

rank7_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/7398']")

rank7_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[7].htm")
driver.back()
time.sleep(5)

rank8_monkey = driver.find_element("css selector",
                                "a[href='/assets/ethereum/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/2646']")

rank8_monkey.click()
time.sleep(5)
saveString(driver.page_source, "bayc_[8].htm")
driver.back()
time.sleep(5)


driver.quit()

##################################################################################################################
################################## Question 3 ####################################################################
ape_name_list = []
ape_bg_list = []
ape_cloth_list = []
ape_earing_list = []
ape_eyes_list = []
ape_fur_list = []
ape_hat_list = []
ape_mouth = []

for i in range(1, 9):
    monkey_file_name = "bayc_[" + str(i) + "].htm"
    monkeys = loadString(monkey_file_name)
    monkey_page = BeautifulSoup(monkeys, "html.parser")

    #### Extract the ape's name
    for i in monkey_page:
        content = i.text
        content_raw = str(content)
        ape_name = content_raw[:4]
        ape_name_list.append(ape_name)

    #### Extract the ape's attributes:
    background = re.findall("Background([A-z ]+)", content_raw)
    ape_bg_list.append(background)

    clothes = re.findall("Clothes([A-z ]+)", content_raw)
    ape_cloth_list.append(clothes)

    earings = re.findall("Earring([A-z ]+)", content_raw)
    ape_earing_list.append(earings)

    eyes = re.findall("Eyes([A-z ]+)", content_raw)
    ape_eyes_list.append(eyes)

    fur = re.findall("Fur([A-z ]+)", content_raw)
    ape_fur_list.append(fur)

    hat = re.findall("Hat([A-z ]+)", content_raw)
    ape_hat_list.append(hat)

    mouth = re.findall("Mouth([A-z ]+)", content_raw)
    ape_mouth.append(mouth)

#### Build the dataframe:
ape_name_list_df = pd.DataFrame(ape_name_list)
ape_bg_list_df = pd.DataFrame(ape_bg_list)
ape_cloth_list_df = pd.DataFrame(ape_cloth_list)
ape_earing_list_df = pd.DataFrame(ape_earing_list)
ape_eyes_list_df = pd.DataFrame(ape_eyes_list)
ape_fur_list_df = pd.DataFrame(ape_fur_list)
ape_hat_list_df = pd.DataFrame(ape_hat_list)
ape_mouth_df = pd.DataFrame(ape_mouth)

q3_df = pd.concat(
    [ape_name_list_df, ape_bg_list_df, ape_cloth_list_df, ape_earing_list_df, ape_eyes_list_df, ape_fur_list_df,
     ape_hat_list_df, ape_mouth_df], axis=1)

q3_df.columns = ["name", "background", "clothes", "earrings", "eyes", "fur", "hat", "mouth"]
print(q3_df)

conn = MongoClient("mongodb://localhost:27017/")
db = conn["sf_pizzerias"]
table = db["sf_pizzerias"]
x = table.insert_many(q3_df.to_dict(orient='records'))



##################################################################################################################
################################## Question 4 ####################################################################
pizza_url = "https://www.yellowpages.com/search?search_terms=Pizzeria&geo_location_terms=San%20Francisco%2C%20CA"
header = {'User-Agent': 'Mozilla/5.0'}
time.sleep(10)
page_top30 = requests.get(pizza_url, headers=header)

# Create a beautifulsoup object
q4_search_result = BeautifulSoup(page_top30.content, "html.parser")
filename_q4 = "sf_pizzeria_search_page.htm"
saveString(q4_search_result, filename_q4)
time.sleep(10)

##################################################################################################################
################################## Question 5 ####################################################################

file_q5 = loadString(filename_q4)
soup_page_q5 = BeautifulSoup(file_q5, "html.parser")

#### Extract the rank and the name
rank = soup_page_q5.select("h2.n")
rank_name = []
for i in rank:
    rank_name.append(i.text)

rank_name_list = rank_name[1:31]

name_list = []
for i in range(0, 30):
    name = rank_name_list[i][3:]
    name_list.append(name)

rank_list = []
for i in range(0, 30):
    rank = rank_name_list[i][:2]
    index = str(rank)
    index2 = re.sub("\.", "", index)
    rank_list.append(index2)

#### Extract the star rating If It Exists
shop_url = soup_page_q5.select("a.business-name")
urls = []
for i in shop_url:
    urls.append(i['href'])
url_list = urls[1:31]

#### Extract the star rating If It Exists, number of reviews IIE
star_review = soup_page_q5.select("div.info")

shop_item = []
for i in star_review:
    shop_item.append(i)

shop_list = shop_item[1:31]

star_rating_list = []
star_review_list = []

for j in range(0, 30):
    shop = shop_list[j]
    rating_review = shop.select("a.rating.hasExtraRating")
    if len(rating_review) == 0:
        star_rating = " "
        star_review = " "
        star_rating_list.append(star_rating)
        star_review_list.append(star_review)
    elif len(rating_review) == 1:
        star_review_raw = shop.select("span.count")
        for i in star_review_raw:
            star_review = i.text
            star_review_list.append(star_review)

        star_rating_raw = shop.select("div.result-rating")
        string_srr = str(star_rating_raw)
        string_srr2 = string_srr[27:]
        string_srr3 = re.sub("\"></div>]", " ", string_srr2)
        star_rating = string_srr3
        star_rating_list.append(star_rating)
#### Extract the TripAdvisor rating IIE, number of TA reviews IIE:
TA_rating_list = []
TA_review_list = []

for j in range(0, 30):
    shop = shop_list[j]
    TA_rating_review = shop.select("div.ratings")
    TA_string = str(TA_rating_review)
    if "data-tripadvisor" not in TA_string:
        TA_rating = " "
        TA_review = " "
        TA_rating_list.append(TA_rating)
        TA_review_list.append(TA_review)
    elif "data-tripadvisor" in TA_string:
        TA_rating = re.findall("{\"rating\":\"([0-9].[0-9])\"", TA_string)
        TA_review = re.findall(",\"count\":\"([0-9]+)\"", TA_string)
        TA_rating_list.append(TA_rating)
        TA_review_list.append(TA_review)

#### Extract the “$” signs IIE, years in business IIE, review IIE, and amenities IIE
dollar_list = []

for j in range(0, 30):
    shop = shop_list[j]
    shop_string = str(shop)
    if "price-range" not in shop_string:
        dollar_list.append(" ")
    elif "price-range" in shop_string:
        dollar_raw = shop.select("div.price-range")
        for i in dollar_raw:
            dollar_list.append(i.text)

#### years in business IIE
business_list = []

for j in range(0, 30):
    shop = shop_list[j]
    shop_string = str(shop)
    if "years-in-business" not in shop_string:
        business_list.append(" ")
    elif "years-in-business" in shop_string:
        business = shop.select("div.years-in-business")
        for i in business:
            business_list.append(i.text)

#### review IIE, and amenities IIE
review_list = []

for j in range(0, 30):
    shop = shop_list[j]
    shop_string = str(shop)
    if "body with-avatar" not in shop_string:
        review_list.append(" ")
    elif "body with-avatar" in shop_string:
        review = shop.select("p.body")
        for i in review:
            review_list.append(i.text)

amenities_list = []

for j in range(0, 30):
    shop = shop_list[j]
    shop_string = str(shop)
    if "amenities-icons" not in shop_string:
        amenities_list.append(" ")
    elif "amenities-icons" in shop_string:
        amenities_raw = shop.select("span.amenities-icons")
        ar2 = str(amenities_raw)
        ar3 = re.findall("xlink:href=\"(#[a-z]+-[a-z]+-[a-z]+)\"", ar2)
        amenities_list.append(ar3)

#### Create a dataframe:
import pandas as pd

rank_list_df = pd.DataFrame(rank_list)
name_list_df = pd.DataFrame(name_list)
url_list_df = pd.DataFrame(url_list)
star_rating_list_df = pd.DataFrame(star_rating_list)
star_review_list_df = pd.DataFrame(star_review_list)
TA_rating_list_df = pd.DataFrame(TA_rating_list)
TA_review_list_df = pd.DataFrame(TA_review_list)
dollar_list_df = pd.DataFrame(dollar_list)
business_list_df = pd.DataFrame(business_list)
review_list_df = pd.DataFrame(review_list)
amenities_list_df = pd.DataFrame(amenities_list)

q5_df = pd.concat([rank_list_df, name_list_df, url_list_df, star_rating_list_df, star_review_list_df, TA_rating_list_df,
                   TA_review_list_df, dollar_list_df, business_list_df, review_list_df, amenities_list_df], axis=1)

q5_df.columns = ["rank", "name", "yp_url", "star_rating", "star_review_count", "TA_rating", "TA_review_count", "price_range", "business_year", "customer_review", "amenities"]

print(q5_df)


##################################################################################################################
################################## Question 6 ####################################################################

conn = MongoClient("mongodb://localhost:27017/")
db = conn["sf_pizzerias"]
table = db["sf_pizzerias"]
x = table.insert_many(q5_df.to_dict(orient='records'))

##################################################################################################################
################################## Question 7 ####################################################################
import re
conn = MongoClient("mongodb://localhost:27017/")

db = conn["sf_pizzerias"]
table = db["sf_pizzerias"]

urls_list = []

q1 = table.find({}, {'yp_url': 1})
for i in q1:
    url_link = "https://www.yellowpages.com" + str(i['yp_url'])
    urls_list.append(url_link)

for j in range(0,30):
    url_linkk = urls_list[j]
    header = {'User-Agent': 'Mozilla/5.0'}
    time.sleep(10)
    shop_top30 = requests.get(url_linkk, headers=header)

    # Create a beautifulsoup object
    q7_search_result = BeautifulSoup(shop_top30.content, "html.parser")
    filename_q7 = "sf_pizzerias_["+ str(j+1) + "].htm"
    saveString(q7_search_result, filename_q7)
    time.sleep(10)

##################################################################################################################
################################## Question 8 ####################################################################
address_list = []
phone_number_list = []
website_list = []

for i in range(1, 31):
    shop_file_name = "sf_pizzerias_[" + str(i) + "].htm"
    shops = loadString(shop_file_name)
    shop_page = BeautifulSoup(shops, "html.parser")

    #### Extract the shop address：
    shop_address = shop_page.select("span.address")
    sa_raw = str(shop_address)
    sa2_1 = re.findall("<span>(.*?)</span>", sa_raw)
    sa2_2 = re.findall("</span>(.*?)</span>", sa_raw)
    sa2 = sa2_1[0] + ' ' + sa2_2[0]
    address_list.append(sa2)

    #### Extract the shop phone number：
    shop_phone_number = shop_page.select("a.phone.dockable")
    for i in shop_phone_number:
        phone_number_list.append(i.text)

    #### Extract the website list：
    shop_website = shop_page.select("a.website-link.dockable")
    if len(shop_website) == 0:
        website_list.append(" ")
    else:
        website_raw = str(shop_website)
        wr2 = re.findall(" href=\"(.*?)\"", website_raw)
        for i in wr2:
            website_list.append(i)

#### Build the dataframe:
address_list_df = pd.DataFrame(address_list)
phone_number_list_df = pd.DataFrame(phone_number_list)
website_list_df = pd.DataFrame(website_list)

q8_df = pd.concat([address_list_df, phone_number_list_df, website_list_df], axis=1)
q8_df.columns = ["address", "phone_number", "website"]

print(q8_df)

##################################################################################################################
################################## Question 9 ####################################################################

import http.client, urllib.parse

long_list = []
lat_list = []

for i in address_list:
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': '9c4c64f27b06f83ca66c9e87f32181ef',
        'query': i,
        'limit': 1,
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    q9_result = data.decode('utf-8')
    q9_raw = str(q9_result)
    long = re.findall("longitude\":(-[0-9.]+),", q9_raw)
    lat = re.findall("latitude\":([0-9.]+),", q9_raw)
    long_list.append(long)
    lat_list.append(lat)

long_list_df = pd.DataFrame(long_list)
lat_list_df = pd.DataFrame(lat_list)

q9_df = pd.concat([long_list_df, lat_list_df], axis=1)
q9_df.columns = ["longitude", "latitude"]
print(q9_df)

q9_df2 = pd.concat([q8_df, q9_df], axis=1)


conn = MongoClient("mongodb://localhost:27017/")
db = conn["sf_pizzerias"]
table = db["sf_pizzerias"]
print(address_list[1], phone_number_list[1], website_list[1], long_list[1], lat_list[1])
for i in range(1, 31):
    x = table.update_many({'rank': str(i)},
                          {"$set": {'address': address_list[i - 1], 'phone': phone_number_list[i - 1],
                                    'website': website_list[i - 1], 'longitude': long_list[i - 1],
                                    'latitude': lat_list[i - 1]}})


