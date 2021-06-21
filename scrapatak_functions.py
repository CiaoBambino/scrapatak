import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import os
import re
import csv

"""
There are 15 functions. ONLY get_all_category, create_folder, get_books_url_from_category and scrap_target_page
get call in the main in the following order.
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
                    s = re.sub('index.html$', 'page-1.html', correct_link)
                    category_link.append(s)
                    category_name.append(ouput)

        return category_link, category_name


def get_books_url_from_category(category_link):
    """
    This function take the category link list and use it to make a 2D list with all the books product page link's
    It also look for other pages to scrap on the same category
    It return the 2D list
    """

    i = 0
    j = len(category_link)
    book_links_per_category = [[] for x in range(j)]    # liste de liste contenant les liens de chaques catégories

    for link in category_link:    # pour chaque lien(catégorie)

        result = requests.get(link)

        if result.status_code == 200:

            soup = BeautifulSoup(result.content, features='html.parser')
            lis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})    # récupère url des livres

            for li in lis:

                b = li.find('a')
                url = b['href']
                incorrectlink = str(url)[8:]
                book_links_per_category[i].append('http://books.toscrape.com/catalogue' + incorrectlink)

            boolnext = next_button(link)

            if boolnext:

                boolnext, next_page_link = next_button(link)
                next_page = requests.get(next_page_link)

                if next_page.status_code == 200:

                    soup = BeautifulSoup(next_page.content, features='html.parser')
                    alllis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

                    for allli in alllis:

                        a = allli.find('a')
                        urls = a['href']
                        incorrectlink = str(urls)[8:]
                        book_links_per_category[i].append('http://books.toscrape.com/catalogue' + incorrectlink)

                    boolnext = next_button(next_page_link)

                    while boolnext:

                        boolnext, next_page_link = next_button(next_page_link)
                        next_page = requests.get(next_page_link)

                        if next_page.status_code == 200:

                            soup = BeautifulSoup(next_page.content, features='html.parser')
                            olis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

                            for oli in olis:

                                a = oli.find('a')
                                urlss = a['href']
                                incorrectlink = str(urlss)[8:]
                                book_links_per_category[i].append('http://books.toscrape.com/catalogue' + incorrectlink)

                            boolnext = next_button(next_page_link)

                            if boolnext:

                                boolnext, next_page_link = next_button(next_page_link)

                                next_button_response = next_button(next_page_link)

                                if next_button_response == False:    # it's the last page

                                    next_page = requests.get(next_page_link)

                                    if next_page.status_code == 200:

                                        soup = BeautifulSoup(next_page.content, features='html.parser')
                                        ollis = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

                                        for olli in ollis:
                                            a = olli.find('a')
                                            urlsss = a['href']
                                            incorrectlink = str(urlsss)[8:]
                                            book_links_per_category[i].append('http://books.toscrape.com/catalogue'
                                                                              + incorrectlink)
                                        break

                                else:
                                    continue
                            else:
                                break
                        else:
                            break
            i += 1
    return book_links_per_category


def scrap_target_page(book_links_per_category, category_name):
    """
    This function scrap the targeted page ,sleep for 3 between 5s each time
    and then write all in a CSV file
    """
    compteur = 0

    for i in range(len(book_links_per_category)):

        name = category_name[i]
        filename = "%s.csv" % name
        directory_name = "%s" % name
        complete_name = os.path.join(directory_name, filename)

        with open(complete_name, 'w') as f:
            fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_taxe',
                          'price_excluding_taxe', 'number_available', 'product_description', 'category',
                          'review_rating', 'image_url']
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()

        for j in range(len(book_links_per_category[i])):


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
            compteur += 1
            print(compteur)

            with open(complete_name, 'a', newline="", encoding='utf8') as f:
                contenu = (product_page_url, universal_product_code, title, price_including_taxe, price_excluding_taxe,
                           number_available, product_description, category, review_rating, image_url)
                writer = csv.writer(f)
                writer.writerow(contenu)
            sleep(randint(3, 5))


def create_folder(category_name):
    """
    This function create all the folder with name in the same order that it get scrapped on the main page of the website
    """

    for names in category_name:

        name = names
        directory_name = "%s" % name

        os.mkdir(directory_name)




def next_button(link):
    """
    This function is doing 2 things :
    - First look for "Next" button that mean we have others pages to scrap and return true if its the case
    - Second get the link of the next page and return it
    """

    result = requests.get(link)

    if result.status_code == 200:

        soup = BeautifulSoup(result.content, features='html.parser')

        child_tag = soup.find('li', {'class': 'next'})
        finlink = link[-10:]
        stringindex = "index.html"

        if finlink == stringindex:

            if child_tag:

                a = child_tag.find('a')
                next_page = a['href']
                next_page_link = str(link[:-10] + next_page)

                result = requests.get(next_page_link)

                if result.status_code == 200:
                    return True, next_page_link

            else:

                return False

        else:
            if child_tag:

                a = child_tag.find('a')
                next_page = a['href']
                next_page_link = str(link[:-11] + next_page)

                result = requests.get(next_page_link)

                if result.status_code == 200:
                    return True, next_page_link

            else:

                return False


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
            j += 1  # incrémente le compteur du tableau pour passer à la clef-valeur suivante

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
        # new_argument = argument_modifier[1:]   supprime le caractere Â devant le prix en livre Â£51.5...
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
        virgule = ","
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
        review_rating = soup.findAll('p', {'class': 'star-rating'})

        return review_rating


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


def get_img(url, title, category_name, i):
    """
    This function download image with the title of the book in name in the folders of the programme
    var i correspond to the position in the 2D list use in the scrap_target_page functions so names matches.
    """
    name = category_name[i]
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
