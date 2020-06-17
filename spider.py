
from datastruct.bst import TreeNode, AvlTree
import webUtils as web



# Dictionary of popular search engines
searchEngines = {
    'google': "www.google.com",
    'duckduckgo': "www.duckduckgo.com"
}



'''
Gets a set of links (a tags with href attributes) 

Recursive function with a given maximum recursion depth.

Scraps a page with a given URL, recurses down any url NOT in 
blackSet or if depth <= 0
'''
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