import re

'''
Gets the Protocol for a given URL.

Returns the Index of the Protocol in the form:
    (startIndex, endIndex)
'''
def getProtocol(url):
    protoMatch = re.match('^\w+:/+', url)
    if protoMatch != None:
        return protoMatch.span()
    else:
        return (0, 0)

'''
Gets the Domain for a given URL 

Optional Parameter: 
    start => Where in the URL to start the search for the domain.

Returns the Index of the Domain in the form:
    (startIndex, endIndex)
'''
def getDomain(url, start=0):
    domainMatch = re.match('^[\.\w]+', url[start:])
    if domainMatch != None:
        return (start, (start + domainMatch.end()))
    else:
        return (0, 0)

'''
Gets the Protocol and Domain substrings from a given URL

The Strings are returned in the format:
    (protocol, domain)
'''
def getProtocolDomain(url):
    protocolSpan = getProtocol(url)
    domainSpan = getDomain(url, protocolSpan[1])
    return (url[protocolSpan[0]:protocolSpan[1]], url[domainSpan[0]:domainSpan[1]])

'''
Extracts the trailing query string from a URL, if any

Returns a tuple in the form:
    (url_without_query, query_string)
'''
def separateQuery(queryURL):
    match = re.search('([=?&][a-zA-Z0-9-_~\.%]*)+$', queryURL)
    if match == None:
        return queryURL, None
    else:
        start, end = match.span()
        return queryURL[0:start], queryURL[start:end]

'''
Adds the Protocol and Domain onto any url if necessary in order to standardize
all URLs.
'''
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

'''
Detects if a url is Relative given a URL and a domain string.

Used to detect if a scrapped link needs to be turned into an absolute link.
'''
def isRelativeURL(url, domainStr):
    return re.match('^\.+', url) or not (re.match('^[a-zA-Z][a-z-A-Z\.-]*://+', url) or re.match('^' + domainStr, url))

'''
Standardize the URLs using the multiple methods above.
'''
def standardizeURL(link, curURL, domainStr, protocolStr="http://"):
    if isRelativeURL(link, domainStr):
        if re.match('/$', curURL):
            url = curURL + link
        else:
            url = curURL + "/" + link
        return preppendDomain(url, domainStr, protocolStr)
    else:
        return preppendDomain(link, domainStr, protocolStr)
