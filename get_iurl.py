import requests
from bs4 import BeautifulSoup

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




