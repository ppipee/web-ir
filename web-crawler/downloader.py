import requests
import re

from requests.exceptions import HTTPError
from config import HEADERS


def getPage(url):
    text = ''
    try:
        response = requests.get(url, headers=HEADERS, timeout=3)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}', url)  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}', url)  # Python 3.6
    else:
        # print('Success!')
        text = response.text
    return text.lower()


def getRobots(url):
    robots_url = url + '/robots.txt'
    robots = getPage(robots_url)

    return robots


def isRobots(raw):
    is_robots = re.search('[uU][sS][eE][rR]-[aA][gG][eE][nN][tT]', raw)

    return not not is_robots


def hasSitemap(raw):
    has_sitemap = re.search('[sS][iI][tT][eE][mM][aA][pP]', raw)

    return not not has_sitemap
