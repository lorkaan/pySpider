from .datastruct.bst import TreeNode, AvlTree
from .datastruct.general import MaxHeap
from . import webUtils as web
#from .webUitls import separateQuery, getSoup, standardizeURL

'''
Used to represent a url location with multiple query strings
'''
class Link:

    def __init__(self, url):
        url, qStr = web.separateQuery(url)
        self.url = url
        self.query = set()
        self.addQuery(qStr)

    def addQuery(self, qString):
        if qString != None and len(qString) > 0:
            self.query.add(qString)

    def __str__(self):
        objStr = f"{self.url}\n"
        for q in self.query:
            objStr = objStr + f"\t{q}\n"
        return objStr

    def __contains__(self, elem):
        return elem in self.query

    def __eq__(self, other):
        if isinstance(other, Link):
            return self.url == other.url
        else:
            nonqStr, _ = web.separateQuery(other)
            return self.url == nonqStr

    def __lt__(self, other):
        if isinstance(other, Link):
            return self.url < other.url
        else:
            nonqStr, _ = web.separateQuery(other)
            return self.url < nonqStr

    def __gt__(self, other):
        if isinstance(other, Link):
            return self.url > other.url
        else:
            nonqStr, _ = web.separateQuery(other)
            return self.url > nonqStr

    def __le__(self, other):
        if isinstance(other, Link):
            return self.url <= other.url
        else:
            nonqStr, _ = web.separateQuery(other)
            return self.url <= nonqStr

    def __ge__(self, other):
        if isinstance(other, Link):
            return self.url >= other.url
        else:
            nonqStr, _ = web.separateQuery(other)
            return self.url >= nonqStr

'''
A function passed to AvlTree, used to ensure the data held by the Tree is
a Link Object.
'''
def createLink(url):
    return Link(url)

'''
A function passed to AvlTree, used to resolve clashes in URLs, 
so that multiple query strings can be associated with the same location.
'''
def resolveClash(url, node):
    if isinstance(node.data, Link):
        _, qStr = web.separateQuery(url)
        node.data.addQuery(qStr)
    else:
        node.data = createLink(url)
    return node

'''
Determines if a given URL  is in a Link Tree

A Link Tree is defined as AvlTree<Link>
'''
def inLinkTree(url, tree):
    preQ, qStr = web.separateQuery(url)
    node = tree.search(preQ)
    if node == None:
        return False
    elif qStr == None or len(qStr) == 0:
        return True
    else:
        link = node.data
        if link == None:
            return False
        else:
            return qStr in link.query


def queueUpHrefs(url, pQueue, bTree, depth):
    if depth <= 0:
        return pQueue
    else:
        protocol, domain = web.getProtocolDomain(url)
        href_list = web.extractHrefs(web.getSoup(url))
        for href in href_list:
            hrefElem = web.standardizeURL(href, url, domain, protocol)
            if inLinkTree(hrefElem, bTree):
                continue
            else:
                pQueue.add(hrefElem, (depth-1))
        return pQueue

'''
Returns a self-balanced tree representing various urls and their 
query strings, if any, found though exploration of hrefs.

A Link Tree is defined as AvlTree<Link>
'''
def createLinkTree(startURL, maxDepth=0):
    tree = AvlTree(clashFunc=resolveClash, addFunc=createLink)
    priorityQueue = MaxHeap()
    priorityQueue.add(startURL, maxDepth)
    depth, currentURL = priorityQueue.next()
    while currentURL != None and (depth != None or depth > 0):
        tree.add(currentURL)
        priorityQueue = queueUpHrefs(currentURL, priorityQueue, tree, depth)
        depth, currentURL = priorityQueue.next()
    return tree

def getRelatedList(url):
    tree = createLinkTree(url)
    return tree.generateList()

'''
if __name__ == '__main__':
    url = 'https://www.google.com/search?q=lists+in+python&oq=lists+in+python&aqs=chrome..69i57j0l7.9755j0j8&sourceid=chrome&ie=UTF-8'
    tree = createLinkTree(url)
    treeList = tree.generateList()
    for elem in treeList:
        print(elem)
'''
