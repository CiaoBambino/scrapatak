import requests
import BeautifulSoup


def get_rr(url):
    result = requests.get(url)
    review_rating = None

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

        review_rating = argument[6]
    return review_rating