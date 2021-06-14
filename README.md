# scrapatak


__Scrapatak__ is a python programm that aim to scrapp some informations of every products on the website : http://books.toscrape.com/index.html
It also create a new folder with logical name for each category of books on the website, and place one CSV file per category containing the informations of all the books concerned into it.
About the informations collected to be more precise it's collecting those informations on the product page of every books : 
* product_page_url 
* universal_product_code 
* title 
* price_including_taxe
*  price_excluding_taxe 
*  number_available 
*  product_description 
*  category 
*  review_rating 
*  image_url
*  and the image of the book itself

The process it taking about one hour due to the fact that we are waiting between 3 and 5 second after each books to not get ban by the server.

## Installation using venv and pip

1. Clone this repository using $ git clone clone https://github.com/CiaoBambino/scrapatak (you can also download the code using as a zip file)
2. Move to the scrapatak root folder with $ cd scrapatak
3. Create a virtual environment for the project with $ python -m venv venv(<---the name you want) on windows or $ python3 -m venv venv on macos & linux.
4. Activate the virtual environment with $ env\Scripts\activate on windows or $ source env/bin/activate on macos & linux.
5. Install project dependencies with $ pip install -r requirements.txt

## How is it working (globaly)

Scrapatak is made of 15 functions.
There are 4 principal functions that get use in the main.py
And 11 sub-fonctions.

1. We define the target (http://books.toscrape.com/index.html)
2. We create 2 lists containing all the links and names of each categories
3. We create all the folder to store our result in the programme directory
4. We create a 2D list with all links from all books for all categories
5. we scrap all this using the 2D list

You can find this schema looking in the main.py 


