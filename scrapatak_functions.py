import requests
from bs4 import BeautifulSoup
import csv

"""
THIS CONTAIN ALL THE FUNCTIONS NECESSARY TO SCRAP PAGES 
"""

def next_button(link):
    """
    This functions is doing 2 things :
    - First look for "Next" button that mean we have others pages to scrap and return true if its the case
    - Second get the link of the next page and return it
    """
    soupsoja = BeautifulSoup(link.text)  # pas besoin de tester le lien déjà fait dans le main
    childTag = soupsoja.find('li', {'class': 'next'})

    if childTag:

        a = childTag.find('a')
        next_page = a['href']
        result = requests.get(b)

        if result.status_code == 200:

            return True, next_page

def scrap_current_page(url):
    """
    This function scrap the current page and return a CSV file
    """
    product_page_url = url
    universal_product_code = get_universal_product_code(url)
    title = get_title(url)
    price_including_tax = get_price_including_taxe(url)
    price_excluding_tax = get_price_excluding_taxe(url)
    number_available = get_number_available(url)
    product_description = get_product_description(url)
    category = get_category(url)
    review_rating = get_review_rating(url)
    image_url = get_image_url(url)
    get_img(image_url)
    csvmaker(product_page_url, universal_product_code, title, price_including_tax,
             price_excluding_tax, number_available, product_description,
             category, review_rating, image_url)

def get_universal_product_code(url):
    """
    This function take the UPC and put it in a list in first place
    """
    result = requests.get(url)
    universal_product_code = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": 0, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1  # incrémente le compteur du tableau pour passer à la clef-valeur suivante

        universal_product_code = argument[0]
    return universal_product_code

def get_title(url):
    """
    This function take the title of the book
    """
    result = requests.get(url)
    title = "unknow"

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        title = soup.find('h1').get_text()
    return title

def get_price_including_taxe(url):
    """
    This function take the price including taxe and put it in a list in fourth place
    """
    result = requests.get(url)
    price_including_tax = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": 0, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1

        price_including_tax = argument[3]
    return price_including_tax

def get_price_excluding_taxe(url):
    """
    This function take the price excluding taxe and put it in a list in third place
    """
    result = requests.get(url)
    price_excluding_tax = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": 0, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1

        price_excluding_tax = argument[2]
    return price_excluding_tax

def get_number_available(url):
    """
    This function take the number available of books and put it in a list in sixs place
    """
    result = requests.get(url)
    number_available = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": 0, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1

        number_available = argument[5]
    return number_available

def get_product_description(url):
    """
    This function take the product description and return it
    """
    result = requests.get(url)
    product_description = "Empty"
    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        p = soup.find('p').get_text()     # peut etre un .string
        product_description = p
    return product_description

def get_category(url):
    """
    This function take the categorie of the books on the product page and return it
    """
    result = requests.get(url)

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        category = "Unknow"
        lis = soup.findALl('li')
        for li in lis:
            a = li.find('a')
            c = a.string
            category += c
            print(category)
        category.replace('HomeBooks', '')
        return category

def get_review_rating(url):
    """
    This function take the review rating number and put it in a list in seventh place and return it
    """
    result = requests.get(url)
    review_rating = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": 0, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1

        review_rating = argument[6]
    return review_rating

def get_image_url(url):
    """
    This function take image link and return it
    """
    result = requests.get(url)
    image_url = "unknow"

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        divs = soup.findAll('div')
        for div in divs:
            img = div.find('img')
            print(img)
            link = img['src']
            image_url = link
    return image_url

def get_img(url):
    """
    This function download image with the title in name in the folders of the programme
    """
    image_name = get_title(url)
    link = get_image_url(url)
    response = requests.get(link)
    if response.status_code == 200:
        with open(image_name + '.jpg', 'wb') as f:
            f.write(response.content)

def csvmaker(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, \
             number_available, product_description, category, review_rating, image_url):
    """
    This function take all the resuslt of others fucntion and put it ine CSV file in the programme folder
    """
    with open('page_info.csv', 'a', newline="") as f:
        fieldnames = ['product_page_url', 'universal_product_code', 'title, price_including_tax', 'price_excluding_tax', \
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        csw_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csw_writer.writeheader()
        f.write(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available\
                , product_description, category, review_rating, image_url)