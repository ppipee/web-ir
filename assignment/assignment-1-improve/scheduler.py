import re
from analyzer import getPath
from urllib.parse import urlsplit, parse_qs
from constants import WORDS_HIGH_PRIORITY


def enqueue(urls, queue, urls_visited):
    url_number = 0

    for url in urls:
        if(url in queue or isUrlVisited(urls_visited, url)):
            continue
        if(isHighPriority(url)):
            queue.insert(0, url)
        else:
            queue.append(url)

    return url_number


def dequeue(frontier_q):
    current_url = frontier_q[0]
    frontier_q.pop(0)

    return current_url


def isHighPriority(url):
    for word in WORDS_HIGH_PRIORITY:
        found = re.search(word, url)

        if (found):
            return True

    return False


def isUrlVisited(urls_visited, url):
    path, _ = getPath(url)

    if(path not in urls_visited):
        return False

    return True


def updateUrlsVisited(urls_visited, url):
    path, _ = getPath(url)

    urls_visited.append(path)
