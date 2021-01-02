from analyzer import getPath, isKuHost, getHost
from urllib.parse import urlsplit, parse_qs
import re


def enqueue(urls, queue, urls_visited):
    number = 0

    for url in urls:
        if(url in queue or not isKuHost(url) or isUrlVisited(urls_visited, url)):
            continue
        if(isHighPriority(url)):
            queue.insert(0, url)
        else:
            queue.append(url)

        number += 1

    return number


def dequeue(frontier_q):
    current_url = frontier_q[0]
    frontier_q.pop(0)

    return current_url


def isHighPriority(url):
    patterns = ['cpe.ku.ac.th', 'cpe']

    for pattern in patterns:
        found = re.search(pattern, url)

        if (found):
            return True

    return False


def isUrlVisited(urls_visited, url):
    query = urlsplit(url).query
    path, _ = getPath(url)

    if(path not in urls_visited.keys()):
        return False

    if(query != ''):
        query = parse_qs(query)

    queries = urls_visited[path]

    if(query not in queries):
        return False

    return True


def updateUrlsVisited(urls_visited, url):
    query = urlsplit(url).query
    path, _ = getPath(url)

    if(query != ''):
        query = parse_qs(query)

    if(path in urls_visited.keys()):
        queries = urls_visited[path]

        if(query not in queries):
            queries.append(query)

    else:
        urls_visited[path] = [query]
