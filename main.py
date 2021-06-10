from functions import create_folder, get_all_category, get_books_url_from_category, scrap_target_page

cible = 'http://books.toscrape.com/index.html'

create_folder(get_all_category(cible))
scrap_target_page(get_books_url_from_category(get_all_category(cible)))
