#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import re


def get_soup(url):
    """
    Качает по ссылке url и номеру страницы p её содержимое, отдаёт в виде bs4
    """    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup


def get_general_information(soup):
    """
    Скачиваем общую инфу о хате
    """
    info = soup.find_all('ul', {'class': 'a10a3f92e9--list--2M4V-'})
    describe = info[0].find_all('li')

    d = {}
    for i in range(len(describe)):
        y = describe[i].find_all('span')
        if len(y) == 2:
            d[y[0].text] = y[1].text
        else:
            d[y[0].text.split('+')[0]] = y[-1].text
    return d


def get_about(soup):
    """
    Получаем информацию о доме
    """
    info = soup.find('div', {'class':'a10a3f92e9--column--2oGBs'})
    if info == None:
        return {}
    else:    
        x = info.find_all('div')
        d = {}
        for i in range(len(x) // 3):
            d[x[i * 3 + 1].text] = x[i * 3 + 2].text
        return d


def get_price(soup):
    """
    Вытаскивает цену
    """
    price = soup.find_all('span', {'itemprop':'price'})[0]
    return {"цена": int(re.sub('\D', '', price.text))}


def get_description(soup):
    """
    Находит в soup описание дома
    """
    d = soup.find('p', {'itemprop': 'description'})              
    return {"описание": d.text}


def get_square_info(soup):
    """
    Собирает инфу о квадратуре, этажности и дате постройки из супа
    """
    d = {}
    desc = soup.find_all('div', {'class': 'a10a3f92e9--info-title--2bXM9'})
    info = soup.find_all('div', {'class' : 'a10a3f92e9--info-value--18c8R'})
    for k,v in zip(desc, info):
        d[k.text] = v.text
    return d


def get_address(soup):
    """
    Вытаскивает адрес
    """
    address = soup.find_all('address', {'class':'a10a3f92e9--address--140Ec'})[0]
    return {"адрес": address.text[:-8]}


get_metro = lambda soup: {"метро": [item.text for item in soup.find_all('li', {'data-name':'renderUnderground'})]}
        
    
def get_title(soup):
    offer_title = soup.find('h1', {"data-name": "OfferTitle"}).text
    return {"тайтл": offer_title}


def get_coord(soup):
    a = [item for item in soup.find_all('script', {"type": "text/javascript"}) if 'coord' in str(item)]
    a = str(a[0])
    d = {
        "lat": re.findall('"lat":(\d\d\.\d+)', a)[0],
        "long": re.findall('"lng":(\d\d\.\d+)', a)[0]
    }
    return d
