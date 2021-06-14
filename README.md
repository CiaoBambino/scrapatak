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
It can be remove by suppressing the line 145 ,last line of scrap_target_page function in scrapatak_functions.

## Installation using venv and pip

1. Clone this repository using $ git clone clone https://github.com/CiaoBambino/scrapatak (you can also download the code using as a zip file)
2. Move to the scrapatak root folder with $ cd scrapatak
3. Create a virtual environment for the project with $ python -m venv venv(<---the name you want) on Windows or $ python3 -m venv venv on MacOs & Linux.
4. Activate the virtual environment with $ env\Scripts\activate on windows or $ source env/bin/activate on macos & linux.
5. Install project dependencies with $ pip install -r requirements.txt

## How is it working (globaly)

Scrapatak is made of 15 functions.
There are 4 principal functions that get use in the main.py
And 11 sub-fonctions.

When the programme is running:

1. We define the target (http://books.toscrape.com/index.html)
2. We create 2 lists containing all the links and names of each categories
3. We create all the folder to store our result in the programme directory
4. We create a 2D list with all links from all books for all categories
5. we scrap all this using the 2D list

You can find this schema looking in the main.py 



# scrapatak


__Scrapatak__ est un scripte python qui vise à récolter certaines informations du site : http://books.toscrape.com/index.html
Le programme créer un nouveau dossier avec un nom en rapport avec les informations récolter et ce pour chaques catégories du site. Il y place un fichier CSV contenant toutes les informations des livres de la catégorie concernée.
A propos des informations collecter et pour être plus précis le script récolte sur chaques pages produit : 
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
*  et l'image de la couverture du livre

Le programme prend environ une heure pour s'éxecuter entièrement du à une commande visant à attendre 3 à 5 secondes entre chaques livres pour ne pas se faire bannir par le serveur suite à un nombre trop important de requêtes dans un temps imparti.
Il est possible de supprimer ce temps d'attente en effaçant la ligne 145 de scrapatak_functions. Elle correspond à la dernière ligne de code de la fonction scrap_target_page

## Installation en utilisant venv et pip

1. Cloner ce dépôt de code à l'aide de la commande $ git clone clone https://github.com/CiaoBambino/scrapatak (vous pouvez également télécharger le code en temps qu'archive zip)
2. Rendez-vous depuis un terminal à la racine du répertoire avec $ cd scrapatak
3. Créer un environnement virtuel pour le projet avec $ python -m venv venv(<---the name you want) sur Windows ou $ python3 -m venv venv Sur MacOs & Linux.
4. Activez l'environnement virtuel avec $ env\Scripts\activate sur Windows ou $ source env/bin/activate sur MacOs & Linux.
5. Installez les dépendances du projet avec la commande $ pip install -r requirements.txt

## Comment ça marche

Scrapatak est composé de 15 fonctions.
Il y en a 4 principales qui sont utilisé dans le main.py.
Et 11 sous fonctions.

Quand le programme est lancé :

1. Il défini la cible (http://books.toscrape.com/index.html)
2. Créer deux listes contenant respectivement, l'url de chaque catégorie et le nom de chaques catégories.
3. Créer tout les dossiers dans lesquels nous allons stocker nos futures données et ce dans le dossier d'exécution du programme.
4. Créer une liste à deux dimensions contenant les liens menant à chaques pages produit pour chaques catégories.
5. Récolte les informations en utilisant cette liste à deux dimensions.

Vous pouvez trouver ce schéma en regardant le main.py 


