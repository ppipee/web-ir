import re
from urllib.parse import urljoin, urlsplit, unquote
from constants import FILE_BLACKLISTS, WORD_BLACKLISTS


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


def isKuHost(url):
    hostname = urlsplit(url).netloc
    found_ku = re.search('ku.ac.th', hostname)

    return not not found_ku


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


def linkParser(raw_html):
    raw_links = getLinks(raw_html)
    links = []

    for link in raw_links:
        if validateLink(link):
            links.append(link)

    return links


def urlsNormalization(hostname, urls):
    urls_normalized = []

    for url in urls:
        _, url_normalize = getPath(url, True)  # remove self-ref

        if(url_normalize == ''):
            continue

        url_normalize = urljoin(hostname, url_normalize)
        url_normalize = unquote(url_normalize)

        if(isKuHost(url_normalize)):
            urls_normalized.append(url_normalize)

    return urls_normalized


def getPath(seed_url, withScheme=False):
    split_url = urlsplit(seed_url)
    path = removeTrialingSlash(split_url.netloc+split_url.path)
    full_path = path

    # if(split_url.query != ''):
    #     full_path = path + '?'+split_url.query

    if(withScheme and split_url.scheme != ''):
        scheme = split_url.scheme + '://'
        path = scheme + path
        full_path = scheme + full_path

    return path, full_path


def getHost(seed_url):
    url = seed_url
    words = ['www.', 'www3.']

    for word in words:
        url = url.replace(word, '')

    split_url = urlsplit(url)
    hostname = split_url.netloc

    if (split_url.scheme == ''):
        return hostname, hostname

    return hostname, split_url.scheme + '://' + hostname


def removeTrialingSlash(url):
    if(len(url) < 1):
        return url

    if (url[-1] == '/'):
        return url[:-1]
    return url
