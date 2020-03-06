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


def get_about(soup):
    '''
    Получаем информацию о доме
    '''
    all = soup.find('div', {'class':'a10a3f92e9--column--2oGBs'})
    x = all.find_all('div')

    d = dict()

    for i in range(len(x)//3):
        d[x[i*3+1].text] = x[i*3+2].text
    return d



def get_price(soup):
    price = soup.find_all('span', {'itemprop':'price'})[0]
    return int(re.sub('\D', '', price.text))

def get_description(soup):
    """
        Находит в soup описание дома
    """
    d = soup.find('p', {'itemprop': 'description'})
                    
    return d.text

def to_info(soup):
    """
        Собирает инфу о квадратуре, этажности и дате постройки из супа
    """
    text = { }
    desc = soup.find_all('div', {'class': 'a10a3f92e9--info-title--2bXM9'})
    info = soup.find_all('div', {'class' : 'a10a3f92e9--info-value--18c8R'})
    for k,v in zip(desc, info):
        text[k.text] = v.text
    return(text)


def get_address(soup):
    address = soup.find_all('address', {'class':'a10a3f92e9--address--140Ec'})[0]
    return(address.text[:-8])
