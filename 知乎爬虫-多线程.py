from bs4 import BeautifulSoup
import urllib

import requests
import random
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import MySQLdb
import asyncio
import aiohttp
from multiprocessing import Pool


MYSQL_DB = '127.0.0.1'
MYSQL_PORT =3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'


def get_header():
    user_agent = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    ]
    header = {"User-Agent": random.choice(user_agent)}
    return header


def get_html(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def get_people(url):
    print('>>>>', url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find_all('div', attrs={'class': 'ContentItem-main'})
    for div in divs:
        aa = div.find('a', attrs={'class': 'UserLink-link'})
        img = aa.find('img')['srcset'].split(' ')[0]
        rich = div.find('div', attrs={'class': 'RichText'})
        aa = aa.find_next('a', attrs={'class': 'UserLink-link'})
        name = aa.get_text()
        uid = aa['href'].split('/')[-1]
        try:
            shuoshuo = '"' + rich.get_text() + '"'
        except:
            shuoshuo = ''
        spans = div.find_all('span', attrs={'class': 'ContentItem-statusItem'})
        span1 = spans[0].get_text().split(' ')[0]
        span2 = spans[1].get_text().split(' ')[0]
        span3 = spans[2].get_text().split(' ')[0]
        button = div.find('button').get_text()
        sex = 1 if button == '关注他' else 0

        print(url, name, uid, shuoshuo, span1, span2, span3, sex )


def get_pages(url):
    header = get_header()
    html = requests.get(url, headers=header).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    buttons = soup.find_all('button', class_='Button PaginationButton Button--plain')
    return int(buttons[-1].get_text())


if __name__ == '__main__':
    url = 'https://www.zhihu.com/people/excited-vczh/following'
    count = get_pages(url)
    urls = []

    pool = Pool()
    for i in range(1, count):
        urls.append('https://www.zhihu.com/people/excited-vczh/following?page=' + str(i))
    pool.map(get_people, urls)



