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



