from datastruct.bst import TreeNode, AvlTree
from datastruct.general import MaxHeap
import webUtils as web

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
        if len(qString) > 0:
            self.query.add(qString)

    def __str__(self):
        objStr = "{self.url}\n"
        for q in self.query:
            objStr = objStr + "\t{q}\n"
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
    link = tree.search(preQ)
    if link == None:
        return False
    elif qStr == None or len(qStr) == 0:
        return True
    else:
        return qStr in link


'''
Recursive helper function for systematically 
exploring the paths from a given URL
'''
def recursiveCreateLinkTree(url, tree, depth):
    if depth == 0:
        return tree
    elif depth < 0:
        # Option for adding more complex searching (like only from a given domain)
        return tree
    else:
        protocol, domain = getProtocolDomain(url)


def queueUpHrefs(url, pQueue, bTree, depth):
    protocol, domain = web.getProtocolDomain(url)
    href_list = web.extractHrefs(web.getSoup(url))
    for href in href_list:
        hrefElem = web.standardizeURL(url, href, domain, protocol)
        if inLinkTree(hrefElem, bTree):
            continue
        else:
            pQueue.add(hrefElem, depth)
    return pQueue

'''
Returns a self-balanced tree representing various urls and their 
query strings, if any, found though exploration of hrefs.

A Link Tree is defined as AvlTree<Link>
'''
def createLinkTree(startURL, maxDepth=3):
    tree = AvlTree(clashFunc=resolveClash, addFunc=createLink)
    priorityQueue = MaxHeap()
    priorityQueue.add(startURL, maxDepth)
    depth, currentURL = priorityQueue.next()
    while currentURL != None and (depth != None or depth > 0):
        tree.add(currentURL)
        priorityQueue = queueUpHrefs(currentURL, priorityQueue, tree, (depth-1))
        depth, currentURL = priorityQueue.next()
    return tree

if __name__ == '__main__':
    url = 'http://www.google.com'
    tree = createLinkTree(url)
    treeList = tree.generateList()
    for elem in treeList:
        print(elem)