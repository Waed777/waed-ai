import requests
from bs4 import BeautifulSoup

def scrape_global_data():
    """
    Scrapes live book data from a public website.
    Returns a list of dictionaries with Title and Price.
    """
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("article", class_="product_pod")
    data = []

    for item in items:
        title = item.h3.a["title"]
        price = item.find("p", class_="price_color").text
        data.append({"Title": title, "Price": price})

    return data
