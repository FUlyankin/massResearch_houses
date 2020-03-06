import requests
from bs4 import BeautifulSoup
import re


def get_soup(url):
    """
        Качает по ссылке url и номеру страницы p её содержимое, отдаёт в виде bs4
    """    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)
    return soup


def get_general_information(soup):
    '''
    Скачиваем общую инфу о хате
    '''
    info = soup.find_all('ul', {'class':'a10a3f92e9--list--2M4V-'})
    
    
    describe = info[0].find_all('li')
    
    dic = collections.defaultdict()
    
    
    for i in range(len(describe)):
        y = describe[i].find_all('span')
        if len(y) == 2:
            dic[y[0].text] = y[1].text
        else:
            dic[y[0].text.split('+')[0]] = y[2].text
    
    
    return(dic)
