import requests
from bs4 import BeautifulSoup
import csv

"""
THIS CONTAIN ALL THE FUNCTIONS TO SCRAP PAGES 
"""

def get_upc(url):
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

def get_pit(url):
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

def get_pet(url):
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

def get_na(url):
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

def get_pd(url):
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

def get_cat(url):
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

def get_rr(url):
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

def get_iurl(url):
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
    url = get_iurl(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_name, 'wb') as f:
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