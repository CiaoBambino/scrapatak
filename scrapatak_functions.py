import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import os
import re
import csv

"""
There are 16 functions. only : get_all_category, create_folder, get_books_url and scrap_page get call in the main.py in 
the following order.
"""


def get_all_category(cible):
    """
    this function take all the category from the main page of the website and return 2 list :
    - one for category names
    - one for category links
    """

    result = requests.get(cible)

    if result.status_code == 200:

        category_link = []
        category_name = []
        soup = BeautifulSoup(result.content, features='html.parser')
        lis = soup.findAll('li')[3:53]

        for li in lis:

            for a in li.findAll('a', href=True):

                if a.text:
                    link = a['href']
                    b = a.get_text()
                    ouput = re.sub(r"[\n\t\s]*", "", b)
                    correct_link = ('http://books.toscrape.com/' + link)
                    category_link.append(correct_link)
                    category_name.append(ouput)

        return category_link, category_name


def create_folder(category_name):
    """
    This function create all the folder with name in the same order that it get scrapped on the main page of the website
    """

    for names in category_name:
        name = names
        filename = "%s.csv" % name
        directory_name = "%s" % name

        os.mkdir(directory_name)

        complete_name = os.path.join(directory_name, filename)

        with open(complete_name, 'w') as f:
            fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_taxe',
                          'price_excluding_taxe', 'number_available', 'product_description', 'category',
                          'review_rating', 'image_url']
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()


def if_next_page(link):
    """
    This function is looking for a "next button" and return true or false
    """
    result = requests.get(link)

    if result.status_code == 200:

        soup = BeautifulSoup(result.content, features='html.parser')

        child_tag = soup.find('li', {'class': 'next'})

        if child_tag:
            return True

        else:
            return False


def get_next_button_url(link):
    """
    This function get the link of the next page and return it
    """
    result = requests.get(link)

    if result.status_code == 200:

        soup = BeautifulSoup(result.content, features='html.parser')

        child_tag = soup.find('li', {'class': 'next'})
        a = child_tag.find('a')
        next_page = a['href']
        comparelink = "index.html"
        next_page_link = "ERROR : get_next_button_url"

        if link[-10:] == comparelink:
            next_page_link = str(link[:-10] + next_page)

        else:
            next_page_link = str(link[:-11] + next_page)

        result = requests.get(next_page_link)

        if result.status_code == 200:
            return next_page_link


def get_books_url(category_link):
    """
    This function take all the urls from books of the website
    """
    book_page_url = []
    for link in category_link:

        result = requests.get(link)

        if result.status_code == 200:

            soup = BeautifulSoup(result.content, features='html.parser')
            lis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

            for li in lis:
                b = li.find('a')
                url = b['href']
                incorrectlink = str(url)[8:]
                book_page_url.append('http://books.toscrape.com/catalogue' + incorrectlink)

            current_page_link = link
            is_other_page = if_next_page(current_page_link)

            while is_other_page:

                next_page_link = get_next_button_url(current_page_link)
                current_page_link = next_page_link
                result = requests.get(next_page_link)

                if result.status_code == 200:

                    soup = BeautifulSoup(result.content, features='html.parser')
                    lis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

                    for li in lis:
                        b = li.find('a')
                        url = b['href']
                        incorrectlink = str(url)[8:]
                        book_page_url.append('http://books.toscrape.com/catalogue' + incorrectlink)

                    is_other_page = if_next_page(current_page_link)

                else:
                    break

    return book_page_url


def scrap(book_page_url):
    """
    This function scrap the targeted page ,sleep for 3 between 5s each time
    and then write all in a CSV file (i put sleep function in comment to go faster)
    """

    compteur = 0

    for url in book_page_url:

        product_page_url = url
        universal_product_code = get_universal_product_code(url)
        title = get_title(url)
        price_including_taxe = get_price_including_taxe(url)
        price_excluding_taxe = get_price_excluding_taxe(url)
        number_available = get_number_available(url)
        product_description = get_product_description(url)
        category = get_category(url)
        review_rating = get_review_rating(url)
        image_url = get_image_url(url)
        get_img(image_url, title, category)

        compteur += 1
        print(compteur)

        name = category
        filename = "%s.csv" % name
        directory_name = "%s" % name
        complete_name = os.path.join(directory_name, filename)

        with open(complete_name, 'a', newline="", encoding='utf8') as f:
            contenu = (product_page_url, universal_product_code, title, price_including_taxe, price_excluding_taxe,
                       number_available, product_description, category, review_rating, image_url)
            writer = csv.writer(f)
            writer.writerow(contenu)
        # sleep(randint(3, 5))


def get_universal_product_code(url):
    """
    This function take the Universal Product Code (UPC) from the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1  # incr??mente le compteur du tableau pour passer ?? la clef-valeur suivante

        universal_product_code = argument[0]
        return universal_product_code


def get_title(url):
    """
    This function take the title of the book from the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')
        title = soup.find('h1').get_text()
        return title


def get_price_including_taxe(url):
    """
    This function take the price including taxe from the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1

        # argument_modifier = str(argument[3])
        # new_argument = argument_modifier[1:]
        price_including_taxe = argument[3]
        return price_including_taxe


def get_price_excluding_taxe(url):
    """
    This function take the price excluding taxe from the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:

            argument[j] = tr.find('td').string
            j += 1

        # argument_modifier = str(argument[2])
        # new_argument = argument_modifier[1:]   supprime le caractere ?? devant le prix en livre ????51.5...
        price_excluding_taxe = argument[2]

        return price_excluding_taxe


def get_number_available(url):
    """
    This function take the number available of books from the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1

        number_available = argument[5]
        return number_available


def get_product_description(url):
    """
    This function take the product description from the product page and return it modified to not include ","
    that are use in CSV files
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')
        paragraphe = soup.findAll('p')[3]
        p = paragraphe.get_text()
        virgule = ",;"
        for char in virgule:  # supprime les virgules pour le csv
            p = p.replace(char, "")
        product_description = p
        return product_description


def get_category(url):
    """
    This function take the category of the book from the product page and return it modified to not get the surplus of
    tabulation, spaces and carriage return
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')
        li = soup.findAll('li')[2]
        a = li.get_text()
        output = re.sub(r"[\n\t\s]*", "", a)
        category = output
        return category


def get_review_rating(url):
    """
    This function take the review rating from the product page and convert it as x/5 and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')
        stars = soup.findAll('p', {'class': 'star-rating'})
        counter = 0
        review_rating = []

        for star in stars:
            i = star.attrs['class'][1]

            if str(i) == "One":
                counter = 1

            elif str(i) == "Two":
                counter = 2

            elif str(i) == "Three":
                counter = 3

            elif str(i) == "Four":
                counter = 4
            else:
                counter = 5

            note = " sur 5"
            review_rating.append(str(counter) + note)

        return review_rating[0]


def get_image_url(url):
    """
    This function take image link from the image on the product page, modify it to be correct and return it
    """
    result = requests.get(url)
    image_url = "unknow"

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.content, features='html.parser')

        images = soup.findAll('img')
        image_url = []

        for image in images:
            link = image['src']
            firstlink = str(link)[6:]
            newlink = "http://books.toscrape.com/" + firstlink
            image_url.append(newlink)
        return image_url[0]


def get_img(url, title, category):
    """
    This function download image with the title of the book in name in the folders of the programme corresponding
    """
    name = category
    default_name = "%s" % title
    a = '"><:|?*.\/'
    for char in a:  # for chars in espace: default_name = default_name.replace(chars, "_")
        default_name = default_name.replace(char, "")
    image_name = default_name.capitalize()
    image_name += ".jpg"
    response = requests.get(url)
    directory_name = "%s" % name

    complete_name = os.path.join(directory_name, image_name)

    if response.status_code == 200:

        with open(complete_name, "wb") as file:
            file.write(response.content)
