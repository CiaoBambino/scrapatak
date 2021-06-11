import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import os
import re
import csv

"""
THIS CONTAIN ALL THE FUNCTIONS NECESSARY TO SCRAP PAGES 
"""


def get_all_category(cible):

    result = requests.get(cible)

    if result.status_code == 200:

        category_link = []
        category_name = []
        soup = BeautifulSoup(result.text, features='html.parser')
        lis = soup.findAll('li')[3:53]

        for li in lis:

            for a in li.findAll('a', href=True):

                if a.text:

                    link = a['href']
                    b = a.get_text()
                    ouput = re.sub(r"[\n\t\s]*", "", b)
                    category_link.append('http://books.toscrape.com/' + link)
                    category_name.append(ouput)

        return category_link, category_name


def get_books_url_from_category(category_link):

    i = 0
    j = len(category_link)
    book_links_per_category = [[] for x in range(j)]    # liste de liste contenant les liens de chaques catégories

    for link in category_link:    # pour chaque lien(catégorie)

        result = requests.get(link)

        if result.status_code == 200:

            soup = BeautifulSoup(result.text, features='html.parser')
            lis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})    # récupère url des livres

            for li in lis:

                b = li.find('a')
                url = b['href']
                firstlink = str(url)[8:]
                book_links_per_category[i].append('http://books.toscrape.com/catalogue' + firstlink)

            if next_button(link) is True:  # s'il y a un bouton next donc une seconde page

                _, next_page_link = next_button(link)  # on peut faire comme ça aussi "function()[1]"

                next_page = requests.get(next_page_link)

                if next_page.status_code == 200:

                    soup2 = BeautifulSoup(next_page.text, features='html.parser')

                    for lii in soup2.findALl('li', {
                                            'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):  # on réitère l'opération

                        a = lii.find('a')
                        urls = a['href']
                        secondfirstlink = str(urls)[8:]
                        book_links_per_category[i].append('http://books.toscrape.com/catalogue' + secondfirstlink)

                    while next_button(next_page_link) is True:  # tant qu'il y a un bouton next

                        _, next_page_link = next_button(next_page_link)
                        another_next_page = requests.get(next_page_link)

                        if another_next_page.status_code == 200:

                            soup3 = BeautifulSoup(another_next_page.text, features='html.parser')

                            for li in soup3.findALl('li', {
                                                    'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):

                                a = li.find('a')
                                urlss = a['href']
                                thrdfirstlink = str(urlss)[8:]
                                book_links_per_category[i].append('http://books.toscrape.com/catalogue' + thrdfirstlink)

            i += 1
    return book_links_per_category


def scrap_target_page(book_links_per_category, category_name):
    """
    This function scrap the targeted page and return a CSV file and sleep for 3 between 7s each time end
    and then write all in a CSV file
    """

    for i in range(len(book_links_per_category)):

        for j in range(len(book_links_per_category[i])):

            name = category_name[i]
            url = book_links_per_category[i][j]
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
            get_img(image_url, title, category_name, i)
            filename = "%s.csv" % name
            directory_name = "%s" % name

            complete_name = os.path.join(directory_name, filename)

            with open(complete_name, 'a', encoding='utf8') as f:     # en mode 'a' pour écrire à la suite
                f.write(product_page_url + universal_product_code + title + price_including_taxe +
                        price_excluding_taxe + number_available + product_description + category + review_rating +
                        image_url)

            sleep(randint(3, 7))


def create_folder(category_name):

    for names in category_name:

        name = names
        directory_name = "%s" % name

        os.mkdir(directory_name)
        filename = "%s.csv" % name

        complete_name = os.path.join(directory_name, filename)

        with open(complete_name, 'w', newline="") as f:
            fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_taxe',
                          'price_excluding_taxe', 'number_available', 'product_description', 'category',
                          'review_rating', 'image_url']
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()


def next_button(link):
    """
    This function is doing 2 things :
    - First look for "Next" button that mean we have others pages to scrap and return true if its the case
    - Second get the link of the next page and return it
    """

    result = requests.get(link)

    if result.status_code == 200:

        soup = BeautifulSoup(result.text, features='html.parser')

        child_tag = soup.find('li', {'class': 'next'})

        if child_tag:

            a = child_tag.find('a')
            next_page = a['href']
            newlink = link.replace("index.html", next_page)
            result = requests.get(newlink)

            if result.status_code == 200:
                return True, newlink

        else:

            return False


def get_universal_product_code(url):
    """
    This function take the UPC and put it in a list in first place
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1  # incrémente le compteur du tableau pour passer à la clef-valeur suivante

        universal_product_code = argument[0]
        return universal_product_code


def get_title(url):
    """
    This function take the title of the book
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')
        title = soup.find('h1').get_text()
        return title


def get_price_including_taxe(url):
    """
    This function take the price including taxe and put it in a list in fourth place
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1

        argument_modifier = str(argument[3])
        new_argument = argument_modifier[1:]  # supprime le caractere Â devant le prix en livre Â£51.5...
        price_including_tax = new_argument
        return price_including_tax


def get_price_excluding_taxe(url):
    """
    This function take the price excluding taxe and put it in a list in third place
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:

            argument[j] = tr.find('td').string
            j += 1

        argument_modifier = str(argument[2])
        new_argument = argument_modifier[1:]  # supprime le caractere Â devant le prix en livre Â£51.5...
        price_excluding_tax = new_argument

        return price_excluding_tax


def get_number_available(url):
    """
    This function take the number available of books and put it in a list in sixs place
    """
    result = requests.get(url)

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')

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
    This function take the product description and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')
        paragraphe = soup.findAll('p')[3]
        p = paragraphe.get_text()
        product_description = p
        return product_description


def get_category(url):
    """
    This function take the categorie of the books on the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')
        li = soup.findAll('li')[2]
        a = li.get_text()
        output = re.sub(r"[\n\t\s]*", "", a)
        category = output
        return category


def get_review_rating(url):
    """
    This function take the review rating number and put it in a list in seventh place and return it
    """
    result = requests.get(url)

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')
        stars = soup.find_all('p', {'class': 'star-rating'})
        counter = 0

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

        note = "/5"
        review_rating = str(counter) + note
        print(review_rating)
        return review_rating


def get_image_url(url):
    """
    This function take image link and return it
    """
    result = requests.get(url)
    image_url = "unknow"

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')

        images = soup.findAll('img')
        for image in images:
            link = image['src']
            firstlink = str(link)[6:]
            image_url = "http://books.toscrape.com/" + firstlink
        return image_url


def get_img(url, title, category_name, i):
    """
    This function download image with the title in name in the folders of the programme
    """
    name = category_name[i]
    image_name = "%s.jpg" % title
    response = requests.get(url)
    directory_name = "%s" % name

    complete_name = os.path.join(directory_name, image_name)

    if response.status_code == 200:

        with open(complete_name, "wb") as file:
            file.write(response.content)
