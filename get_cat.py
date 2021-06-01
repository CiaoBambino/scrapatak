import requests
import BeautifulSoup

def get_cat(url):
    result = requests.get(url)

    if result.status_code == 200:  # le resultat est vrai on continu (result.ok)
        print(result)

        soup = BeautifulSoup(result.text)
        category = "Unknow"
        lis = soup.findALl('li')
        for li in lis:
            a = li.find('a')
            c += str(a.string)
            category = c
            print(category)
        category.replace('HomeBooks', '')
