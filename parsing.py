import requests
from bs4 import BeautifulSoup


def parsing():
    page = requests.get("https://www.maa.org/news/on-this-day").text
    soup = BeautifulSoup(page, "html.parser")

    listy = []

    for news in soup.find_all("div", {"class": "field-content"}):
        result = news.text.split("\n")[0]
        listy.append(result)
    return listy
