# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 01:10:27 2022

@author: User
"""
# Структура массива из функции INFORMATION [автор, дата, название,[тэг(1), тэг(2), ...., тэг(n)], ссылка]

import requests
from bs4 import BeautifulSoup as bs

def MAIN_HTML():
    URL_TEMPLATE = "https://rg.ru/tema/bezopasnost"
    r = requests.get(URL_TEMPLATE)
    return r.text

def LINKS(html):   #возвращает ссылки на последние 32 новости в виде массива
    A = []
    soup = bs(html, "html.parser")
    NEWS = soup.find_all('a', class_='ItemOfListStandard_title__eX0Jw')
    for name in NEWS:
        if 'https:' in name['href']:
            A.append(name['href'])
        else:
            A.append('https://rg.ru' + name['href'])
    return A

def INFORMATION(x):   # на вход требует ссылку, а по ней возвращает массив нужных нам данных по 1ой новости
    '''

    :param x: Ссылка на новость
    :return: [автор, дата, название, [тэг(1), тэг(2), ...., тэг(n)], ссылка]
    '''
    B = [''] * 5
    B[3] = []
    B[4] = x
    SUBPAGE_URL = x
    k = requests.get(SUBPAGE_URL)
    sub_soup = bs(k.text, "html.parser")
    AUTHOR = sub_soup.find_all('a', class_='LinksOfAuthor_item__LtcAf')
    for sub_name in AUTHOR:
        B[0] = sub_name.text.split('(')[0].rstrip()   #adds THE AUTHOR
    if not B[0]:
        B[0] = 'Не указан'
    TAGS = sub_soup.find_all('div', class_='PageArticleContent_relationBottom__N2VjE')
    for tag in TAGS:
        t = tag.find_all('a')
        for k in t:
            B[3].append(k.text)   #adds tags
    DATE = sub_soup.find_all('div', class_= ['PageArticleContent_date__yoeGq', 'EditorialPageArticleContent_date__Wohyy'])
    for dat in DATE:
        B[1] = dat.text[:10]   #adds date
    TITLE = sub_soup.find_all('h1', class_= ['PageArticleContent_title__RVnvC', 'EditorialPageArticleContent_title__NHNkn'])
    for tit in TITLE:
        B[2] = tit.text   #adds title oth event
    return B
