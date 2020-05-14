import requests
from bs4 import BeautifulSoup


def get_catalog(url_link: str) -> dict:
    print("Starting web scraping https://krepkoshop.com/category/")
    urls = []
    category_list= []
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    category = soup.find_all('div', {'class': 'catalog-block'})
    for cat in category:
        urls.append(url_link + str(cat.find('a')['href']).replace('/category/', ''))
        category_list.append(cat.find('span').string)
    catalog = dict(zip(category_list, urls))
    print("Web scraping done")
    return catalog

def get_products(catalog_name: str, url_link: str) -> list:
    print("Starting  web scraping {}".format(url_link))
    url_home = 'https://krepkoshop.com'
    product_list = []
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    catalog = soup.find_all('div', {'class': 'product-blb-name'})
    for card in catalog:           
        product = {
            'name': '',
            'old_price': 0,
            'sale': 0,
            'price': 0,
            'category': catalog_name,
            'url': ''
        }
        product['name'] = card.find('h5', {'itemprop': 'name'}).find('span').string.replace('\n', ' ')
        product['url'] = url_home + str(card.find('a', {'class': 'product-name'})['href'])
        product['price'] = int(card.find('span', {'class':'price nowrap'}).contents[0].strip(' руб.').replace(' ',''))
        if card.find('span', {'class':'sale-compare-block'}):
            product['old_price'] = int(card.find('span', {'class':'compare-at-price nowrap'}).string.strip(' руб.').replace(' ',''))
            product['sale'] = int(card.find('span', {'class':'sale-compare-block'}).contents[1].string.lstrip(' (-').rstrip('%)'))
        else:
            product['old_price'] = product['price']   
        product_list.append(product)
    print("Web scraping done")
    return product_list

def start_scrape():
    category_list = []
    product_list = []
    check_names = []
    #krepko site
    catalog = get_catalog("https://krepkoshop.com/category/")
    for category in catalog:
        products = get_products(category, catalog[category])
        category_list.append(products)
    for category in category_list:
        for product in category:
            if product['name'] not in check_names:
                product_list.append(product)
                check_names.append(product['name'])
    return(product_list)

start_scrape()
