import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import os
import re


"""
THIS CONTAIN ALL THE FUNCTIONS NECESSARY TO SCRAP PAGES 
"""


def get_all_category(cible):

    result = requests.get(cible)

    if result.status_code == 200:

        category_link = []
        category_name = []
        soup = BeautifulSoup(result.text, features='html.parser')
        litag = soup.findAll('li')

        for li in litag[2:]:
            for link in li.findAll('a')
                a = link.get('href')
                links = a
                b = a.get_text()
                ouput = re.sub(r"[\n\t\s]*", "", b)
                category_link.append('http://books.toscrape.com/' + links)
                category_name.append(ouput)
                print(links)
        print(category_name)
        return category_link, category_name14


def get_books_url_from_category(category_link):

    i = 1
    j = len(category_link)
    book_links_per_category = [[] for x in range(j)]    # liste de liste contenant les liens de chaques catégories

    for link in category_link:    # pour chaque lien(catégorie)

        current_category = requests.get(link)

        if current_category.status_code == 200:

            soup = BeautifulSoup(current_category.text)

            for li in soup.findALl('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):    # récupère url des livres

                b = li.find('a')
                url = b['href']
                book_links_per_category[i].append(url)
                next_page_link = None

            if next_button(link) is True:  # s'il y a un bouton next donc une seconde page

                _, next_page_link = next_button(link)  # on peut faire comme ça aussi "function()[1]"

                next_page = requests.get(next_page_link)

                if next_page.status_code == 200:

                    soup2 = BeautifulSoup(next_page.text)

                    for li in soup2.findALl('li', {
                                            'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):  # on réitère l'opération

                        a = li.find('a')
                        urls = a['href']
                        book_links_per_category[i].append(urls)

                    while next_button(next_page_link) is True:  # tant qu'il y a un bouton next

                        _, next_page_link = next_button(next_page_link)
                        another_next_page = requests.get(next_page_link)

                        if another_next_page.status_code == 200:

                            soup3 = BeautifulSoup(another_next_page.text)

                            for li in soup3.findALl('li', {
                                                    'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):

                                a = li.find('a')
                                urlss = a['href']
                                book_links_per_category[i].append(urlss)

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
            get_img(image_url, category_name, i)
            filename = "%s.csv" % name
            save_path = '%s' % name

            complete_name = os.path.join(save_path, filename)

            with open(complete_name, 'a', newline="") as f:     # en mode ajout 'a' pour écrire à la suite
                f.write(product_page_url + universal_product_code + title + price_including_taxe +
                        price_excluding_taxe + number_available + product_description + category + review_rating +
                        image_url)

            sleep(randint(3, 7))


def create_folder(category_name):

    i = 0

    for names in category_name:

        name = category_name[i]
        i += 1
        directory_name = "%s" % name

        os.mkdir(directory_name)
        print(directory_name)
        filename = "%s.csv" % name

        with open(filename, 'w', newline="") as f:
            f.write('product_page_url, universal_product_code, title, price_including_taxe,price_excluding_taxe,\
                    number_available, product_description, category, review_rating, image_url')


def next_button(link):
    """
    This function is doing 2 things :
    - First look for "Next" button that mean we have others pages to scrap and return true if its the case
    - Second get the link of the next page and return it
    """

    next_button_link = requests.get(link)

    if next_button_link.status_code == 200:

        soup = BeautifulSoup(link.text)

        child_tag = soup.find('li', {'class': 'next'})

        if child_tag:

            a = child_tag.find('a')
            next_page = a['href']
            result = requests.get(next_page)

            if result.status_code == 200:

                return True, next_page

        else:

            return False


def get_universal_product_code(url):
    """
    This function take the UPC and put it in a list in first place
    """
    result = requests.get(url)
    universal_product_code = "Unknow"

    if result.status_code == 200:  # result.ok
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

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text, features='html.parser')
        title = soup.find('h1').get_text()
        return title


def get_price_including_taxe(url):
    """
    This function take the price including taxe and put it in a list in fourth place
    """
    result = requests.get(url)
    price_including_tax = "Unknow"

    if result.status_code == 200:  # result.ok
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
    price_excluding_tax = "Unknow"

    if result.status_code == 200:  # result.ok
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
    number_available = "Unknow"

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
    product_description = "Empty"

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

        soup = BeautifulSoup(result.text)
        categorie = []
        lis = soup.findALl('li')

        for li in lis:
            a = li.find('a')
            categorie.append(str(a))

        category = categorie[2]
        return category


def get_review_rating(url):
    """
    This function take the review rating number and put it in a list in seventh place and return it
    """
    result = requests.get(url)
    review_rating = "Unknow"

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "product type": 0, "pricee": 0, "pricei": 0, "tax": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            j += 1

        review_rating = argument[6]
        return review_rating


def get_image_url(url):
    """
    This function take image link and return it
    """
    result = requests.get(url)
    image_url = "unknow"

    if result.status_code == 200:
        print(result)

        soup = BeautifulSoup(result.text)

        divs = soup.findAll('div')
        for div in divs:
            img = div.find('img')
            print(img)
            link = img['src']
            image_url = link
        return image_url


def get_img(url, category_name, i):
    """
    This function download image with the title in name in the folders of the programme
    """
    name = category_name[i]
    image_name = "%s.jpg" % get_title(url)
    link = get_image_url(url)
    response = requests.get(link)
    save_path = '%s' % name

    complete_name = os.path.join(save_path, image_name)

    if response.status_code == 200:

        with open(complete_name, 'wb') as f:
            f.write(response.content)
