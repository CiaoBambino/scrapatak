import requests
from bs4 import BeautifulSoup

def get_title(url):

    result = requests.get(url)
    title = "unknow"

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        title = soup.find('h1').get_text()
    return title