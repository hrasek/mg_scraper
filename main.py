import requests
from bs4 import BeautifulSoup as BS
import re


def find_prices(text):
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

    else:
        text = screen_reader_texts[1].text
    price = find_prices(text)
    return price, discount  # type: ignore


links = [
    "https://cukrfreeshop.cz/produkt/vyhodny-balicek-2-druhu-aroha-horciku-malat-a-bisglycinat/#",
    "https://cukrfreeshop.cz/produkt/vyhodny-balicek-3-druhu-horciku-akce/",
    "https://cukrfreeshop.cz/produkt/natios-magnesium-malate-1000-mg-b6/",
    "https://cukrfreeshop.cz/produkt/natios-magnesium-bisglycinate-1000-mg-b6/",
    "https://cukrfreeshop.cz/produkt/aroha-magnesium-bisglycinate/",
    "https://cukrfreeshop.cz/produkt/aroha-magnesium-malate/",
]


for link in links:
    price, discount = price_scraper(link)
    print(price, discount)
