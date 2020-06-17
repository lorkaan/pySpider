from datastruct.bst import TreeNode, AvlTree
import webUtils as web

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

def createLink(url):
    return Link(url)

def resolveClash(url, node):
    if isinstance(node.data, Link):
        _, qStr = web.separateQuery(url)
        node.data.addQuery(qStr)
    else:
        node.data = createLink(url)
    return node

def recursiveGetLinkTree(url, tree):
    pass

def getLinkTree(startURL):
    tree = AvlTree(clash=resolveClash, addFunc=createLink)
    return recurisveGetLinkTree(startURL, tree)

if __name__ == '__main__':
    url = 'http://www.google.com'