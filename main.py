from bs4 import BeautifulSoup
from selenium import webdriver
import re
import config

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
my_list=''

def response(name, link, price):
    return (f':squeeze_bottle: Name: [{name}]({link})\nPrice: **{price}**\n')

def stylevana(links, my_list, webhook):
    for link in links:
        driver.get(link)
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, 'lxml')
        name = soup.find('h1', class_='product-name-h1').text
        price = soup.find('span', class_='price', id=re.compile('^product-price')).text.replace('\n', '')
        link = soup.find('link', rel='canonical')['href']
        my_list += response(name, link, price)
    webhook.send('Store: *Stylevana*\n' + my_list)

# HADA LABO

stylevana(config.hada_labo_list, my_list, config.hada_labo_webhook)

# COSRX

stylevana(config.cosrx_list, my_list, config.cosrx_webhook)

driver.quit()