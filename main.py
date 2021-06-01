import requests
import BeautifulSoup4

print("Give URL to scrap with the protocol (http://...) \n")
url = input()
global paths = input("Give path to save resuslt on your storage (/Users/lalala/Desktop/sample.jpg)")

def scrap_for_url(url):

        result = requests.get(url)

        if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
            print(result)

            soup = BeautifulSoup(result.text)
            category = None
            lis = soup.findALl('li')
            for li in lis:
                a = li.find('a')
                c += str(a.string)
                category = c
                print(name_category)
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

    choice = input("What category do you want to scrap ?") #ajout d'un script pour chercher parmis
                                                           # les urls et noms déjà dans le tableau

"""
VARIABLES 

url = input("Give URL to scrap with the protocol ex : http://... \n")
product_page_url = None
universal_product_code = None
title = None
price_including_tax = None
price_excluding_tax = None
number_available = None
product_description = None
category = None
review_rating = None
image_url = None

FONCTIONS 

def scrap_all():
"""