import requests
from bs4 import BeautifulSoup
import csv
from all_function import *

"""
In the following order, Main function is testing the link of the website, taking all the categories links and names,
for each categories links testing them, go inside, take html, find books links and finally scrap each books one bye
one and read into CSV files
"""

cible = 'http://books.toscrape.com/index.html'

result = requests.get(cible)

if result.status_code == 200:  # result.ok
    print(result)

    soup = BeautifulSoup(result.text)
    category = [{"category_name": "Books", "link": "url.html"}]
    i = 1

    for ultag in soup.findAll('ul', {'class': 'nav nav-list'}):    # on récupère les catégorie

        for litag in ultag.findAll('li'):

            links = []
            a = litag.find('a')
            category_name = a.string
            link = a['href']
            links.append(link)
            category[i].append({'category_name': category_name, 'link': link})
            i += 1

            for link in links:      # pour chaque catégorie(lien)

                current_cat = requests.get(link)  # on entre dans la catégorie

                if current_cat.status_code == 200:

                    soupsale = BeautifulSoup(current_cat.text)          # on récupère les liens des livres

                    for li in soupsale.findALl('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):

                        b = li.find('a')
                        url = b['href']
                        product_page_url = url
                        universal_product_code = get_upc(url)
                        title = get_title(url)
                        price_including_tax = get_pit(url)
                        price_excluding_tax = get_pet(url)
                        number_available = get_na(url)
                        product_description = get_pd(url)
                        category = get_cat(url)
                        review_rating = get_rr(url)
                        image_url = get_iurl(url)

                        csvmaker(product_page_url, universal_product_code, title, price_including_tax,
                                 price_excluding_tax, number_available, product_description,
                                 category, review_rating, image_url)

            # write category in csv files
