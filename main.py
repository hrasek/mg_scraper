import requests
from bs4 import BeautifulSoup as BS
import re
link = 'https://cukrfreeshop.cz/produkt/vyhodny-balicek-2-druhu-aroha-horciku-malat-a-bisglycinat/#'
response = requests.get(link)
soup = BS(response.text, "html.parser")
response_text = response.text
price_wrap = soup.find('div', {'class': 'entry-price-wrap'})
screen_reader_texts = price_wrap.find_all('span', {'class': 'screen-reader-text'})
pattern = r'\d+'
price = re.search(pattern, screen_reader_texts[1].text)
buy_it = True if int(price.group(0)) < 900 else False
# if price < 900:


print(screen_reader_texts[1].text, price.group(0), buy_it)