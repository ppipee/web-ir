import re
from urllib.parse import urljoin, urlsplit, unquote


def validateLink(link):
    blacklists = ['.css', '.js', '.json', '.webp', '.xml', '.c', '.cc',
                  '.png', '.jpg', '.svg', '.jpeg', '.tiff',  '.bmp',
                  '.mp3', '.mp4', '.gif', '.ts', '.avi', '.flv', '.mkv', '.ovf', '.vmdk',
                  '.pdf', '.xlsx', '.pptx', '.docx', '.txt', '.ppt',
                  '.zip', '.rar', '.tar.gz', '.deb', '.exe'
                  ]

    for blacklist in blacklists:
        found = re.search(blacklist+'/?$', link)

        if (found):
            return False

    return True


def isKuHost(url):
    found_ku = re.search('ku.ac.th', url)
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

        url_normalize = urlNormalization(hostname, url_normalize)
        urls_normalized.append(url_normalize)

    return urls_normalized


def urlNormalization(hostname, url):
    url_normalize = urljoin(hostname, url)
    url_normalize = unquote(url_normalize)

    return url_normalize


def getPath(seed_url, withScheme=False):
    split_url = urlsplit(seed_url)
    path = removeTrialingSlash(split_url.netloc+split_url.path)
    full_path = path

    if(split_url.query != ''):
        full_path = path + '?'+split_url.query

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
