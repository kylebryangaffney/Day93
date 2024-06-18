from bs4 import BeautifulSoup
import requests

class Saxophone:
    def __init__(self, title, price, link, availability, image_url, sax_type):
        self.title = title
        self.price = price
        self.link = link
        self.availability = availability
        self.image_url = image_url
        self.sax_type = sax_type

    def __str__(self):
        return f"{self.title}, {self.price}, {self.link}, {self.availability}, {self.image_url}, {self.sax_type}"

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "link": self.link,
            "availability": self.availability,
            "image_url": self.image_url,
            "sax_type": self.sax_type
        }

def fetch_saxophones():
    base_url = "https://www.bostonsaxshop.com"
    try:
        response = requests.get(f"{base_url}/saxophones")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching saxophones: {str(e)}")

    bss_soup = BeautifulSoup(response.text, "html.parser")
    all_saxophones = bss_soup.find_all("div", class_="grid-item")
    saxophones = []

    def identify_sax_type(title):
        title_lower = title.lower()
        if 'soprano' in title_lower:
            return 'Soprano'
        elif 'alto' in title_lower:
            return 'Alto'
        elif 'tenor' in title_lower:
            return 'Tenor'
        elif 'baritone' in title_lower:
            return 'Baritone'
        else:
            return 'Unknown'

    for saxophone_div in all_saxophones:
        title_div = saxophone_div.find("div", class_="grid-title")
        price_div = saxophone_div.find("div", class_="product-price")
        link_tag = saxophone_div.find("a", class_="grid-item-link")
        availability_div = saxophone_div.find("div", class_="product-mark sold-out") or saxophone_div.find("div", class_="product-scarcity")
        image_tag = saxophone_div.find("img", class_="grid-item-image")

        title = title_div.getText().strip() if title_div else "No Title"
        price = price_div.getText().strip() if price_div else "No Price"
        link = f"{base_url}{link_tag.get('href')}" if link_tag else "No Link"
        availability = availability_div.getText().strip() if availability_div else "Limited Availability"
        image_url = image_tag['data-image'] if image_tag and 'data-image' in image_tag.attrs else "No Image Available"
        sax_type = identify_sax_type(title)

        saxophone = Saxophone(title, price, link, availability, image_url, sax_type)
        saxophones.append(saxophone)

    return saxophones
