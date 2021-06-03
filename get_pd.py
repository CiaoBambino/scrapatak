import requests
from bs4 import BeautifulSoup

def get_pd(url):
    result = requests.get(url)
    product_description = "Empty"
    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        p = soup.find('p').get.text()     # peut etre un .string
        product_description = p
    return product_description