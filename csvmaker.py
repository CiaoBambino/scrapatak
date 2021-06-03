import requests
from bs4 import BeautifulSoup
import csv

def csvmaker(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):

    with open('page_info.csv', 'a', newline="") as f:
    fieldnames = ['product_page_url', 'universal_product_code', 'title, price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    csw_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csw_writer.writeheader()
    f.write(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)