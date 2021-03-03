import re

from urllib.parse import urlsplit, urljoin, unquote
from constants import FILE_BLACKLISTS, WORD_BLACKLISTS
from urlUtils import removeTrialingSlash, isKuHost


def validateLink(link):
    for blacklist in FILE_BLACKLISTS:
        found = re.search(blacklist+'/?$', link)

        if (found):
            return False

    for blacklist in WORD_BLACKLISTS:
        found = re.search(blacklist, link)

        if (found):
            return False

    return True


def getLinks(raw_html):
    links = []
    anchor_tag = '<a '
    pattern_start = 'href="'
    pattern_end = '"'
    index = 0

    while index < len(raw_html):
        anchor_index = raw_html.find(anchor_tag, index)

        if(anchor_index > 0):
            index = anchor_index + len(anchor_tag)
            start = raw_html.find(pattern_start, index) + len(pattern_start)
            end = raw_html.find(pattern_end, start)

            if(end < start or start < index):
                break

            link = raw_html[start:end]
            link = link.strip()

            if(len(link) > 0):
                links.append(link)

            index = end + len(pattern_end)
        else:
            break

    return links


def linkParser(rawHtml):
    rawLinks = getLinks(rawHtml)
    links = []

    for link in rawLinks:
        if validateLink(link) and isKuHost(link):
            links.append(unquote(link))

    return links


def urlNormalize(url, header):
    splitUrl = urlsplit(url)
    urlNormalized = removeTrialingSlash(splitUrl.netloc+splitUrl.path)

    if(splitUrl.scheme != ''):
        urlNormalized = splitUrl.scheme + '://' + urlNormalized

    if(urlNormalized == ''):
        return urlNormalized

    urlNormalized = urljoin(header, urlNormalized)

    return urlNormalized
