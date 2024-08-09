import requests
from bs4 import BeautifulSoup as BS
import re


def find_price(text: str):
    pattern = r"\d+\s\d+|\d+"
    price = re.search(pattern, text)
    return int(price.group(0).replace(" ", ""))  # type: ignore


def price_scraper(link: str):
    response = requests.get(link)
    soup = BS(response.text, "html.parser")

    price_wrap = soup.find("div", {"class": "entry-price-wrap"})

    screen_reader_texts = price_wrap.find_all("span", {"class": "screen-reader-text"})  # type: ignore
    discount = True if screen_reader_texts else False
    if not discount:
        screen_reader_texts = price_wrap.find_all("span", {"class": "woocommerce-Price-amount"})  # type: ignore
        text = screen_reader_texts[0].text
        regular_price = find_price(text)
        return [regular_price], discount

    else:
        regular_text = screen_reader_texts[0].text
        regular_price = find_price(regular_text)
        discount_text = screen_reader_texts[1].text
        discount_price = find_price(discount_text)
        return [regular_price, discount_price], discount


def scrape_prices():
    LINKS = [
        "https://cukrfreeshop.cz/produkt/vyhodny-balicek-2-druhu-aroha-horciku-malat-a-bisglycinat/#",
        "https://cukrfreeshop.cz/produkt/vyhodny-balicek-3-druhu-horciku-akce/",
        "https://cukrfreeshop.cz/produkt/natios-magnesium-malate-1000-mg-b6/",
        "https://cukrfreeshop.cz/produkt/natios-magnesium-bisglycinate-1000-mg-b6/",
        "https://cukrfreeshop.cz/produkt/aroha-magnesium-bisglycinate/",
        "https://cukrfreeshop.cz/produkt/aroha-magnesium-malate/",
    ]

    DESCRIPTIONS = [
        "2 Mg's combination",
        "3 Mg's combination",
        "Natios Malate",
        "Natios Bisglycinate",
        "Aroha Bisglycinate",
        "Natios Malate",
    ]

    output = []
    for link, description in zip(LINKS, DESCRIPTIONS):
        price, discount = price_scraper(link)
        if discount:
            output.append(
                {
                    "description": description,
                    "price_regular": price[0],
                    "price_discount": price[1],
                    "discount": discount,
                    "link": link,
                }
            )
        else:
            output.append(
                {
                    "description": description,
                    "price_regular": price[0],
                    "discount": discount,
                    "link": link,
                }
            )

    return output
