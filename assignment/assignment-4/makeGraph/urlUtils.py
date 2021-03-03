import re

from urllib.parse import urlsplit
from constants import BASE_PATH


def removeTrialingSlash(url):
    if(len(url) < 1):
        return url

    if (url[-1] == '/'):
        return url[:-1]
    return url


def getPath(seed_url):
    split_url = urlsplit(seed_url)
    path = removeTrialingSlash(split_url.path)

    return path


def isKuHost(url):
    hostname = urlsplit(url).netloc
    found_ku = re.search('ku.ac.th', hostname)

    return not not found_ku


def getHostname(url, withSchema=False):
    words = ['www.', 'www3.']

    for word in words:
        url = url.replace(word, '')

    splitUrl = urlsplit(url)
    hostname = splitUrl.netloc

    if (splitUrl.scheme == ''):
        return hostname

    if(withSchema):
        return splitUrl.scheme + '://' + hostname

    return hostname


def getDirectoryPath(url):
    hostname = getHostname(url)
    path = hostname + getPath(url)

    words = ['http://', 'https://', 'https:',
             'http:', 'www.', 'www3.', '.php', '/index.php']

    for word in words:
        path = path.replace(word, '')

    has_file_type = re.search('/.+\.html$', path)
    if(not has_file_type):
        path += '/index.html'

    return path
