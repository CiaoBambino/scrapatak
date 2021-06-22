from scrapatak_functions import get_all_category, create_folder, get_books_url, scrap


"""
                      THIS IS SCRAPATAK 4.0 
	
+------+.      +------+       +------+       +------+      .+------+
|`.    | `.    |\     |\      |      |      /|     /|    .' |    .'|
|  `+--+---+   | +----+-+     +------+     +-+----+ |   +---+--+'  |
|   |  |   |   | |    | |     |      |     | |    | |   |   |  |   |
+---+--+.  |   +-+----+ |     +------+     | +----+-+   |  .+--+---+
 `. |    `.|    \|     \|     |      |     |/     |/    |.'    | .'
   `+------+     +------+     +------+     +------+     +------+'

The first line is the target
The second line is creating 2 list containing all the links and names of categories
The third line create all the folder to store our result
The fourth line create a list with all links from all books
The fifth line scrap all this

Take around 1 hour
"""

cible = 'http://books.toscrape.com/index.html'

category_link, category_name = get_all_category(cible)
create_folder(category_name)
book_page_url = get_books_url(category_link)
scrap(book_page_url)