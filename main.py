from scrapatak_functions import create_folder, get_all_category, get_books_url_from_category, scrap_target_page

cible = 'http://books.toscrape.com/index.html'

category_link, category_name = get_all_category(cible)
create_folder(category_name)
book_links_per_category = get_books_url_from_category(category_link)
scrap_target_page(book_links_per_category, category_name)
