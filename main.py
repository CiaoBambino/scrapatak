import requests
from bs4 import BeautifulSoup
import csv
from all_function import *

print("Give URL to scrap with the protocol (http://...) \n")
url = input()

product_page_url = get_ppu(url)
universal_product_code = get_upc(url)
title = get_title(url)
price_including_tax = get_pit(url)
price_excluding_tax = get_pet(url)
number_available = get_na(url)
product_description = get_pd(url)
category = get_cat(url)
review_rating = get_rr(url)
image_url = get_iurl(url)

csvmaker(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)

