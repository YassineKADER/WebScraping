#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 12:25:05 2022

@author: yk
"""

# importation section and adding options for the browser
import sys
import csv
from time import sleep
from lxml import html
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
firefoxoptions = Options()
firefoxoptions.add_argument("-headless")
driver = webdriver.Firefox(
    executable_path="geckodriver", options=firefoxoptions)
# get and filter links:


def get_Pages_Links():
    driver.get("https://www.jumia.ma")
    sleep(2)
    tree = html.fromstring(driver.page_source)
    driver.title
    links = driver.find_elements(By.CLASS_NAME, "s-itm")
    pages = []
    for link in links:
        href = str(link.get_attribute("href"))
        if href != "None" and "jumia.ma/services/" not in href:
            pages.append(href)
    return pages

# get the max number of pages inside every page:


def to_digit(value=""):
    return int(''.join(filter(lambda i: i.isdigit(), value)))


def pages_count(link=""):
    driver.get(link)
    n_pages = driver.find_elements(By.CLASS_NAME, "pg")
    last_page_href = 0
    for i in n_pages:
        if str(i.get_attribute("aria-label")) == "Dernière page":
            last_page_href = to_digit(
                str((i.get_attribute("href").split("page=")[1])))
    return last_page_href

# go inside each page and collect data


def collect_data(link="", n_pages=0):
    if n_pages != 0:
        with open('data.csv', "a", encoding="utf16") as file:
            f = csv.writer(file)
            for i in range(n_pages):
                driver.get(link+f"&page={i+1}#catalog-listing")
                print(link+f"&page={i+1}#catalog-listing")
                array = driver.execute_script("return window.__STORE__")
                if array != None:
                    products = array.get('products')
                    if products != None:
                        for product in products:
                            price = product.get('prices')
                            rating = product.get('rating')
                            line = [str(product.get('displayName')), product.get('categories'), product.get('brand'), product.get('isBuyable'),
                                    price.get('price'), price.get('rawprice'), price.get(
                                        'oldprice'), price.get('taxEuro'),
                                    price.get('discount'), rating.get('average'), rating.get('totalRatings')]
                            line = [str(i) for i in line]

                            f.writerow(line)
            file.close()

    else:
        driver.get(link)
        print(link)
        array = driver.execute_script("return window.__STORE__")
        if array != None:
            products = array.get('products')
            if products != None:
                with open('data.csv', "a", encoding="utf16") as file:
                    f = csv.writer(file)
                    for product in products:
                        price = product.get('prices')
                        rating = product.get('rating')
                        line = [product.get('displayName'), product.get('categories'), product.get('brand'), product.get('isBuyable'),
                                price.get('price'), price.get('rawprice'), price.get(
                                    'oldprice'), price.get('taxEuro'),
                                price.get('discount'), rating.get('average'), rating.get('totalRatings')]
                        line = [str(i) for i in line]

                        f.writerow(line)
                    file.close()


columns = ['Name', 'Categories', 'Brand', 'Is_Buyable',
           'Price(dh)', 'RawPrice(dh)', 'OldPrice(dh)', 'Tax(eur)', 'Discount', 'Rating', 'TotalRating']

with open("data.csv", "a", encoding="utf16") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    file.close()

pages = get_Pages_Links()
# print(len(pages))
#n = pages_count(pages[33])

#collect_data(pages[33], n)

for page in pages:
    n = pages_count(page)
    collect_data(page, n)
