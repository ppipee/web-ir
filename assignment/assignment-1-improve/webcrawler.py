import time

from downloader import getPage, getRobots, isRobots, hasSitemap
from analyzer import linkParser, urlsNormalization, getHost, getPath
from scheduler import enqueue, dequeue, updateUrlsVisited
from store import storingHtml, storingTxt, getDirectoryPath

from constants import SEED_URL, MAX_URL_VISITED, URL_ERROR

startTime = time.time()

urls_visited = []
number_of_urls = 0
frontier_queue = [SEED_URL]
seed_url = SEED_URL
robot_hosts = []
robot_visited = []
sitemaps = []
error = 0


def errorOccur():
    global error
    error += 1

    print('error: ', error)
    print('')


def storingRobotsAndSitemaps():
    storingTxt(('\n').join(robot_hosts), 'robots')
    storingTxt(('\n').join(sitemaps), 'sitemaps')
    storingTxt(('\n').join(urls_visited), 'visited')


while len(urls_visited) < MAX_URL_VISITED and len(frontier_queue) > 0:
    # initial
    seed_url = dequeue(frontier_queue)
    print('seed url :', seed_url)

    # downloader
    raw_html = getPage(seed_url)

    if (raw_html == ''):
        errorOccur()
        continue

    hostname, full_hostname = getHost(seed_url)
    path, _ = getPath(seed_url)

    if(path not in urls_visited):
        directory_path = getDirectoryPath(seed_url)
        success = storingHtml(raw_html, directory_path)

        if (not success):
            errorOccur()
            continue

    updateUrlsVisited(urls_visited, seed_url)

    # robot
    if(hostname not in robot_visited):
        raw_robots = getRobots(full_hostname)
        is_robots = isRobots(raw_robots)
        has_sitemap = hasSitemap(raw_robots)

        if(is_robots):
            print('robot : ', hostname)
            robot_hosts.append(hostname)

        if(is_robots and has_sitemap):
            print('sitemap : ', hostname)
            sitemaps.append(hostname)

        robot_visited.append(hostname)

    # analyzer
    if(number_of_urls < MAX_URL_VISITED+URL_ERROR+error):

        links = linkParser(raw_html)

        if (len(links) > 0):
            urls = urlsNormalization(full_hostname, links)
            number = enqueue(urls, frontier_queue, urls_visited)
            print('found url :', number)
            number_of_urls += number

    print('visited : ', len(urls_visited))
    print('queue :', len(frontier_queue))
    print('number of urls : ', number_of_urls)
    print('number of robots :', len(robot_hosts))
    print('number of sitemaps :', len(sitemaps))
    print('')

    if(len(urls_visited) % 100 == 0):
        storingRobotsAndSitemaps()

storingRobotsAndSitemaps()

endTime = time.time()
print('process time : ', endTime-startTime)
