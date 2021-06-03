import requests
from bs4 import BeautifulSoup

def get_cat(url):
    result = requests.get(url)

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        category = "Unknow"
        lis = soup.findALl('li')
        for li in lis:
            a = li.find('a')
            b = a['href']
            c += str(a.string)
            category = c
            print(category)
        category.replace('HomeBooks', '')


def scrap_for_cat(url):

    url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    url_category = []
    name_category = []
    result = requests.get(url)
    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)
        soup = BeautifulSoup(result.text)
        lis = soup.findALl('li')
        for li in lis:
            a = li.find('a')
            b = a['href']
            c = a.string
            url_category.append(b)
            name_category.append(c)
            print(url_category)
            print(name_category)

            [{"category_name": "Action", "url": url.hmtl}]