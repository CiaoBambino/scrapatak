import requests
import BeautifulSoup4


def get_img(url):
    reponse = requests.get(get_iurl(url))
    if reponse.status_code == 200:
        with open('global paths', 'wb') as f:
        f.write(reponse.content)