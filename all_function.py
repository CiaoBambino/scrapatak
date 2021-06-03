import requests
from bs4 import BeautifulSoup
import csv

def get_ppu(url):
    product_page_url = url
    return product_page_url

def get_upc(url):

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

    result = requests.get(url)
    title = "unknow"

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        title = soup.find('h1').get_text()
    return title

def get_pit(url):

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
    result = requests.get(url)
    product_description = "Empty"
    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        p = soup.find('p').get.text()     # peut etre un .string
        product_description = p
    return product_description

def get_cat(url):
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
    image_name = get_title(url)
    url = get_iurl(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_name, 'wb') as f:
        f.write(response.content)

def csvmaker(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, \
             number_available, product_description, category, review_rating, image_url):

    with open('page_info.csv', 'a', newline="") as f:
    fieldnames = ['product_page_url', 'universal_product_code', 'title, price_including_tax', 'price_excluding_tax', \
                  'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    csw_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csw_writer.writeheader()
    f.write(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available\
            , product_description, category, review_rating, image_url)