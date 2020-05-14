import os
import requests
import schedule
import time
import krepko_web_scraper
import db


def compare(product_list: list) -> str:
    compare_list = []
    compare_string = ''
    for card in product_list:
        selector = db.select_product(card['name'])
        if selector['status'] == False:
            product = {
                    'name': card['name'],
                    'old_price': selector['output']['price'],
                    'price': card['price'],
                    'category': card['category'],
                    'url': card['url']
                    }
            compare_list.append(product)
    compare_string = []
    for card in compare_list:
        compare_string.append('наименование: {}\nстарая цена: {}\nцена: {}\nкатегория: {}\nссылка: {}\n-----\n'.format(card['name'], card['old_price'], card['price'], card['category'], card['url']))
    compare_string = ''.join(compare_string)
    return compare_string

def bot_sendtext(bot_message: str) -> None:
	### Send text message
	bot_token = os.environ['TOKEN']
	bot_chatID = os.environ['CHAT_ID']
	send_text = u'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, bot_chatID, bot_message)
	requests.get(send_text)

def db_maintain(product_list: list) -> None:
    db.delete_products()
    for card in product_list:
        db.insert_product(card['name'], card['old_price'], card['sale'], card['price'], card['category'], card['url'])
    return

def start_bot():
    product_list = krepko_web_scraper.start_scrape()
    compare_string = compare(product_list) 
    bot_sendtext(compare_string)
    db_maintain(product_list)
    return

schedule.every(30).minutes.do(start_bot)
while 1:
    schedule.run_pending()
    time.sleep(1)
