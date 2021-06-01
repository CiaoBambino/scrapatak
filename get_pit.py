import requests
import BeautifulSoup4

def get_pit(url):

    result = requests.get(url)
    price_including_tax = None

    if result.status_code == 200:  # result.ok
        print(result)

        soup = BeautifulSoup(result.text)

        trs = soup.findAll('tr')
        argument = {"upc": 0, "None": 0, "pricee": 0, "pricei": o, "None": 0, "available": 0, "review": 0}

        j = 0
        for tr in trs:
            argument[j] = tr.find('td').string
            print(argument + '\n')
            j += 1

        price_including_tax = argument[3]
    return price_including_tax