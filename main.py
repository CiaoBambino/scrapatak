from scrapatak_functions import create_folder, get_all_category, get_books_url_from_category, scrap_target_page


"""
                      THIS IS SCRAPATAK 3.0 
	
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
The fourth line create a 2D list with all links from all books for all categories
The fifth line scrap all this

Take around 1 hour to scrap all because of sleep(randint(3,5))
"""

cible = 'http://books.toscrape.com/index.html'

category_link, category_name = get_all_category(cible)
create_folder(category_name)
book_links_per_category = get_books_url_from_category(category_link)
scrap_target_page(book_links_per_category, category_name)
