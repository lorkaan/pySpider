import requests
from bs4 import BeautifulSoup

'''
Gets a BeautifulSoup Object.
'''
def getSoup(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'lxml')

'''
Extracts the a tags from a given BeauitfulSoup
'''
def extractHrefs(soup):
    a_list = soup.find_all('a')
    hrefList = []
    for elem in a_list:
        try:
            hrefList.append(elem['href'])
        except:
            continue
    return hrefList

def extractText(url):
    return getSoup(url).get_text()