import requests
from bs4 import BeautifulSoup as BS
import re


def find_price(text):
    pattern = r"\d+\s\d+|\d+"
    price = re.search(pattern, text)
    return int(price.group(0).replace(" ", ""))  # type: ignore


def price_scraper(link):
    response = requests.get(link)
    soup = BS(response.text, "html.parser")

    price_wrap = soup.find("div", {"class": "entry-price-wrap"})

    screen_reader_texts = price_wrap.find_all("span", {"class": "screen-reader-text"})  # type: ignore
    discount = True if screen_reader_texts else False
    if not discount:
        screen_reader_texts = price_wrap.find_all("span", {"class": "woocommerce-Price-amount"})  # type: ignore
        text = screen_reader_texts[0].text
        regular_price = find_price(text)
        discount_price = regular_price

    else:
        regular_text = screen_reader_texts[0].text
        regular_price = find_price(regular_text)
        discount_text = screen_reader_texts[1].text
        discount_price = find_price(discount_text)

    return [regular_price, discount_price], discount


def scrape_prices():
    links = [
        "https://cukrfreeshop.cz/produkt/vyhodny-balicek-2-druhu-aroha-horciku-malat-a-bisglycinat/#",
        "https://cukrfreeshop.cz/produkt/vyhodny-balicek-3-druhu-horciku-akce/",
        "https://cukrfreeshop.cz/produkt/natios-magnesium-malate-1000-mg-b6/",
        "https://cukrfreeshop.cz/produkt/natios-magnesium-bisglycinate-1000-mg-b6/",
        "https://cukrfreeshop.cz/produkt/aroha-magnesium-bisglycinate/",
        "https://cukrfreeshop.cz/produkt/aroha-magnesium-malate/",
    ]

    prices = []
    discounts = []
    for link in links:
        price, discount = price_scraper(link)
        prices.append(price)
        discounts.append(discount)
    return prices, discounts
