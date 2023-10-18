from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class": 'B_NuCI'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):
    try:
        price = soup.find("div", class_="_30jeq3 _16Jk6d")

        print(price)

    except:
        price = ""
    return price


def get_rating(soup):
    try:
        rating = soup.find("span", attrs={"class": "_2_R_DZ"})
        title_rating = rating.text

    except:
        title_rating = ""

    return title_rating

# def get_review(soup):
#     try:
#         review = soup.find("span", attrs={"class": "_2_R_DZ"})
#         title_review = review.text

#     except:
#         title_review = ""

#     return title_review


def get_manu(soup):
    try:
        print("reading")
        manuf = soup.find("div", attrs={"class": "_3LWZlK _138NNC"})
        product_manu = manuf.text+" stars"
        print(manuf)
    except:
        product_manu = ""
    return product_manu


if __name__ == '__main__':
    d = {"product_url": [], "title": [],
         "price": [], "rating": [], "Stars": []}
    for i in range(1, 21):
        URL = "https://www.flipkart.com/search?q=bags&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_5_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_5_0_na_na_na&as-pos=5&as-type=HISTORY&suggestionId=bags&requestId=cf867156-cac7-4bf4-b105-705fe310e783&page=" + \
            str(i)
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        # print("Page "+str(i)+" is goin on")
        links = soup.find_all("a", attrs={
            'class': '_2UzuFa'})
        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        for link in links_list:
            p_link = "https://www.flipkart.com" + link
            # print(p_link)
            new_webpage = requests.get(
                p_link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            prices = new_soup.find_all("div", class_="_30jeq3")
        # Function calls to display all necessary product information
            d['product_url'].append([p_link])
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            # d['review'].append(get_review(new_soup))
            d['Stars'].append(get_manu(new_soup))
        flipkart_df = pd.DataFrame.from_dict(d)
        flipkart_df['title'].replace('', np.nan, inplace=True)
        flipkart_df = flipkart_df.dropna(subset=['title'])
        flipkart_df.to_csv("flipkart.csv", header=True, index=False)
