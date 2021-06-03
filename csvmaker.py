import requests
from bs4 import BeautifulSoup

def csvmaker(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
    with open('page_info.csv', 'w') as f:
        for