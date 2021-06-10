import requests
from bs4 import BeautifulSoup
import csv
from scrapatak_functions import next_button, scrap_target_page
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
    category_link = []
    category_name = []
    i = 1

    for ultag in soup.findAll('ul', {'class': 'nav nav-list'}):    # on récupère les catégorie

        for litag in ultag.findAll('li'):

            a = litag.find('a')
            b = a.soup.get_text()
            category_name[i] = b
            link = a['href']
            category_link[i] = link

            for link in category_link:

                name = category_name[i]
                filename = "%s.csv" % name
                directory_name = "%s" % name
                img_directory_name = "IMG_%s" % name

                parent_dir = os.getcwd()    # directory path
                img_parent_dir = os.getcwd()

                path = os.path.join(parent_dir, directory_name)    # path = directory path + names
                img_path = os.path.join(img_parent_dir, img_directory_name)

                os.mkdir(path)    # create folder
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
                            scrap_target_page(url, filename, img_directory_name)

                        if next_button(link) is True:  # if next button so next page so scrap all of them

                            _, next_page_link = next_button(link)  # on peut faire comme ça aussi "function()[1]"
                            scrap_target_page(next_page_link, filename, img_directory_name)

                            while next_button(next_page_link) is True:  # tant qu'il y a un bouton next

                                _, next_page_link = next_button(next_page_link)  # copy next page link
                                scrap_target_page(next_page_link, filename, img_directory_name)

            i += 1  # on incrémente pour passer à la case clef valeur suivante et parcourir les listes
