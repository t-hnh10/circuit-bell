#!/usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import config
import csv
import datetime

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
product_list = ''

f = open('data.csv', 'a')
writer = csv.writer(f)

def response(name, link, price):
    return (f':squeeze_bottle: Name: [{name}]({link})\nPrice: **{price}**\n')

def stylevana(links, product_list, webhook):
    for link in links:
        driver.get(link)
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, 'lxml')
        name = soup.find('h1', class_='product-name-h1').text
        price = soup.find('span', class_='price', id=re.compile('^product-price')).text.replace('\n', '')
        link = soup.find('link', rel='canonical')['href']
        product_list += response(name, link, price)
        writer.writerow([datetime.datetime.now(), name, price, link])
    webhook.send('Store: *Stylevana*\n' + product_list)

def lilabeauty(links, product_list, webhook):
    for link in links:
        driver.get(link)
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, 'lxml')
        name = soup.find('h1', class_='ProductMeta__Title Heading u-h2').text
        price = soup.find('span', class_='ProductMeta__Price Price Price--highlight Text--subdued u-h4').text
        link = soup.find('link', rel='canonical')['href']
        product_list += response(name, link, price)
        writer.writerow([datetime.datetime.now(), name, price, link])
    webhook.send('Store: *Lilabeauty*\n' + product_list)

# HADA LABO

stylevana(config.hada_labo_list, product_list, config.hada_labo_webhook)
lilabeauty(config.hada_labo_list_lilabeauty, product_list, config.hada_labo_webhook)

# COSRX

stylevana(config.cosrx_list, product_list, config.cosrx_webhook)
lilabeauty(config.cosrx_list_lilabeauty, product_list, config.cosrx_webhook)

# Purito

stylevana(config.purito_list, product_list, config.purito_webhook)
lilabeauty(config.purito_list_lilabeauty, product_list, config.purito_webhook)

# Pyunkang Yul

stylevana(config.pyunkang_yul_list, product_list, config.pyunkang_yul_webhook)
lilabeauty(config.pyunkang_yul_list_lilabeauty, product_list, config.pyunkang_yul_webhook)

f.close()
driver.quit()