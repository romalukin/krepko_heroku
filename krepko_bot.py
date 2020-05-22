import os
import requests
import schedule
import time
import krepko_web_scraper
import db


def compare(product_list: list) -> list:
    print("Starting compare")
    compare_list = []
    for card in product_list:
        selector = db.select_product(card['name'])
        if selector['status']:
            if selector['output']['price'] != card['price']:
                product = {
                        'name': card['name'],
                        'old_price': selector['output']['price'],
                        'price': card['price'],
                        'category': card['category'],
                        'url': card['url']
                        }
                compare_list.append(product)
        else:
            product = {
                    'name': '~~~NEW~~~ ' + card['name'],
                    'old_price': card['old_price'],
                    'price': card['price'],
                    'category': card['category'],
                    'url': card['url']
                    }
            compare_list.append(product)
    compare_list_string = []
    for card in compare_list:
        compare_list_string.append('наименование: {}\nцена: {} -> {}\nкатегория: {}\nссылка: {}\n-----\n'.format(card['name'], card['old_price'], card['price'], card['category'], card['url']))
    #compare_string = ''.join(compare_string)
    print("Compare comlete")
    return compare_list_string

def bot_sendtext(bot_message: list) -> None:
    ### Send text message
    print("Sending message")
    bot_token = os.environ['TOKEN']
    bot_chatID = os.environ['CHAT_ID']
    if len(bot_message) > 0:
        for message in bot_message:
            send_text = u'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, bot_chatID, message)
            requests.get(send_text)
            print("Message sent. Message: {}".format(message))
    else:
        print("Nothing has changed. Nothing to send")

def db_maintain(product_list: list) -> None:
    print("Start clearing table in db and inserting new products")
    db.delete_products()
    for card in product_list:
        db.insert_product(card['name'], card['old_price'], card['sale'], card['price'], card['category'], card['url'])
    print("Done clearing and inserting")
    return

def start_bot():
    product_list = krepko_web_scraper.start_scrape()
    compare_list = compare(product_list) 
    bot_sendtext(compare_list)
    db_maintain(product_list)
    return

#schedule.every(2).minutes.do(start_bot)
#while 1:
#    schedule.run_pending()
#    time.sleep(1)
while 1:
    print("Start!!!!!!")
    start_bot()
    print("Sleeping 120 sec")
    time.sleep(120)