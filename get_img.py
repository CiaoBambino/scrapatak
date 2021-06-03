import requests

def get_img(url):
    image_name = get_title(url)
    url = get_iurl(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(global paths, 'wb') as f:
        f.write(response.content)