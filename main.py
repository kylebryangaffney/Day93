from bs4 import BeautifulSoup
import requests

base_url = "https://www.bostonsaxshop.com"

response = requests.get("https://www.bostonsaxshop.com/saxophones")
bss_website = response.text

bss_soup = BeautifulSoup(bss_website, "html.parser")

all_saxophone_titles = bss_soup.find_all(name="div", class_="grid-title")
for i in all_saxophone_titles:
     print(i.getText())

all_saxophone_prices = bss_soup.find_all(name="div", class_="product-price")
for j in all_saxophone_prices:
     print(j.getText())


all_saxophone_hrefs = bss_soup.find_all("a",class_="grid-item-link")
for k in all_saxophone_hrefs:
    print(k.get("href"))