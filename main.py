import requests
from bs4 import BeautifulSoup
import csv
from scrapatak_functions import next_button, scrap_target_page, get_universal_product_code, get_title,\
                                get_price_including_taxe, get_price_excluding_taxe, get_number_available, \
                                get_product_description, get_category, get_review_rating, get_image_url, get_img, \
                                csv_writer

import os

"""
In the following order, Main function is testing the link of the website, taking all the categories links and names,
for each categories links create a csv file, find books links, scrap each books one bye one and write it into CSV 
files and finally look for "next button" and go scrap other page if there is
"""

cible = 'http://books.toscrape.com/index.html'

result = requests.get(cible)

if result.status_code == 200:  # result.ok
    print(result)

    soup = BeautifulSoup(result.text, 'lxml')
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


            for link in links:      # pour chaque catégorie(lien)

                name = category[i]['category_name']                           # names
                filename = "%s.csv" % name
                directory_name = "%s" % name
                img_directory_name = "IMG_%s" % name
                                                                              # directory path
                parent_dir = os.getcwd()
                img_parent_dir = os.getcwd()
                                                                              # path = directory path + names
                path = os.path.join(parent_dir, directory_name)
                img_path = os.path.join(img_parent_dir, img_directory_name)
                                                                              # create folder
                os.mkdir(path)
                os.mkdir(img_path)

                with open(os.path.join(path, filename), 'w', newline="") as f:
                    fieldnames = ['product_page_url', 'universal_product_code', 'title, price_including_tax',
                                  'price_excluding_tax',
                                  'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                    csw_writer = csv.DictWriter(f, fieldnames=fieldnames)
                    csw_writer.writeheader()

                    current_cat = requests.get(link)  # on entre dans la catégorie

                    if current_cat.status_code == 200:

                        soupsale = BeautifulSoup(current_cat.text, 'lxml')      # on récupère les liens des livres

                        for li in soupsale.findALl('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):

                            b = li.find('a')
                            url = b['href']
                            scrap_target_page(url)

                        if next_button(link) == True: # if next button so next page so scrap all of them

                            _, next_page_link = next_button(link) # on peut faire comme ça aussi "function()[1]"
                            scrap_target_page(next_page_link)

                            while next_button(next_page_link) == True: # tant qu'il y a un bouton next

                                _, next_page_link = next_button(next_page_link) # copy next page link
                                scrap_target_page(next_page_link)

            i += 1  # on incrémente pour passé à la case clef valeur suivante et parcourir le dictionnaire