import requests
from bs4 import BeautifulSoup
import re
from avlTree import TreeNode, AvlTree

searchEngines = {
    'google': "www.google.com",
    'duckduckgo': "www.duckduckgo.com"
}

def getSoup(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'lxml')

def extractLinks(soup):
    return soup.find_all('a')

def getProtocol(url):
    protoMatch = re.match('^\w+:/+', url)
    if protoMatch != None:
        return protoMatch.span()
    else:
        return (0, 0)

def getDomain(url, start=0):
    domainMatch = re.match('^[\.\w]+', url[start:])
    if domainMatch != None:
        return (start, (start + domainMatch.end()))
    else:
        return (0, 0)

def getProtocolDomain(url):
    protocolSpan = getProtocol(url)
    domainSpan = getDomain(url, protocolSpan[1])
    return (url[protocolSpan[0]:protocolSpan[1]], url[domainSpan[0]:domainSpan[1]])

def separateQuery(queryURL):
    match = re.search('([=?&][a-zA-Z0-9-_~\.%]*)+$', queryURL)
    if match == None:
        return queryURL, None
    else:
        start, end = match.span()
        return queryURL[0:start], queryURL[start:end]

def preppendDomain(url, domainStr, protocolStr="http://"):
    finalStr = ""
    protoStart, protoEnd = getProtocol(url)
    if protoStart == protoEnd and protoEnd == 0:
        finalStr = protocolStr
    else:
        return url
    domainStart, domainEnd = getDomain(url, protoEnd)
    if domainStart == domainEnd and domainEnd == 0:
        return finalStr + domainStr + url
    else:
        return url

def isRelativeURL(url, domainStr):
    return re.match('^\.+', url) or not (re.match('^[a-zA-Z][a-z-A-Z\.-]*://+', url) or re.match('^' + domainStr, url))

def standardizeURL(link, curURL, domainStr, protocolStr="http://"):
    if isRelativeURL(link, domainStr):
        if re.match('/$', curURL):
            url = curURL + link
        else:
            url = curURL + "/" + link
        return preppendDomain(url, domainStr, protocolStr)
    else:
        return preppendDomain(link, domainStr, protocolStr)

def getLinkSet(url, blackSet, depth=3):
    nonqueryURL, queryURL = separateQuery(url)
    if nonqueryURL not in blackSet:
        blackSet.add(url)
    if depth <= 0:
        return blackSet
    else:
        soup = getSoup(url)
        a_list = extractLinks(soup)
        pStr, dStr = getProtocolDomain(url)
        processQueue = []
        for elem in a_list:
            try:
                elemLink = standardizeURL(elem['href'], url, dStr, pStr)
                nonquery, query = separateQuery(elemLink)
                if nonquery in blackSet:
                    continue
                else:
                    processQueue.append(elemLink)
            except Exception as e:
                continue

        for link in processQueue:
            nonquery, query = separateQuery(link)
            if nonquery in blackSet:
                continue
            else:
                blackSet = getLinkSet(link, blackSet, (depth-1))
        return blackSet

def googleSearch(terms, protocol="http://"):
    pass
     

if __name__ == '__main__':
    #url = 'https://www.google.com/search?sxsrf=ALeKk01DnDrLHD1w1j3Jq3kpOFoRTUVFwQ%3A1592181754858&source=hp&ei=-sPmXuqYMo7M-gSisb7IDw&q=python3+sockets&oq=python3+sockets&gs_lcp=CgZwc3ktYWIQAzIECCMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgQIABAKOgUIABCDAToFCAAQsQM6BwgAELEDEAo6BwgjELACECc6BAgAEA06BggAEA0QClDMU1jscmC0dGgCcAB4AIAByAGIAYgOkgEGMi4xMC40mAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwjq_aefy4LqAhUOpp4KHaKYD_kQ4dUDCAg&uact=5'
    #url = 'https://docs.python.org/3/tutorial/datastructures.html'
    url = 'http://www.google.com'
    linkSet = getLinkSet(url, AvlTree())
    
    for link in linkSet:
        print(link)