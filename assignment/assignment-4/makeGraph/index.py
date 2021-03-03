from parser import urlNormalize, linkParser
from loader import loadFileWithUrl
from urlUtils import getHostname
from constants import START_URL
from store import storingTxt


class WebGraph:
    def __init__(self, startUrl):
        self.urlMapper = {
            startUrl: 0
        }
        self.hashTable = {
            0: []
        }
        self.queue = [startUrl]
        self.currentUrl = ''
        self.visited = {}

    def enqueue(self, urls):
        for url in urls:
            if(url not in self.visited.keys() and url not in self.queue):
                self.queue.append(url)

    def dequeue(self):
        self.currentUrl = self.queue[0]
        self.queue.pop(0)

    def buildTable(self, urls):
        currentUrlIndex = self.urlMapper[self.currentUrl]

        for url in urls:
            urlIndex = len(self.urlMapper)

            if url not in self.urlMapper.keys():
                self.urlMapper[url] = urlIndex
                self.hashTable[urlIndex] = []
            else:
                urlIndex = self.urlMapper[url]

            self.hashTable[currentUrlIndex].append(urlIndex)

    def urlsNormalize(self, links):
        urlHeader = getHostname(self.currentUrl, True)
        urls = []

        for link in links:
            url = urlNormalize(link, urlHeader)

            if(url != ''):
                urls.append(url)

        return urls

    def makeGraph(self):
        # callerList = {}

        # for caller, indexList in self.hashTable.items():
        #     self.hashTable[caller] = list(set(indexList))

        #     if(caller not in callerList.keys()):
        #         callerList[caller] = True

        urlMap = self.urlMapper.keys()
        webGraph = []

        for indexList in self.hashTable.values():
            if(len(indexList) == 0):
                webGraph.append('-')
            else:
                calleeList = [str(index) for index in list(set(indexList))]
                webGraph.append(", ".join(calleeList))

        return urlMap, webGraph

    def run(self):
        roundNumber = 0
        while len(self.queue) > 0:
            roundNumber += 1
            self.dequeue()

            rawHtml = loadFileWithUrl(self.currentUrl)
            self.visited[self.currentUrl] = True

            if(rawHtml == ''):
                continue

            links = linkParser(rawHtml)
            urls = self.urlsNormalize(links)

            self.buildTable(urls)
            self.enqueue(urls)

            if(roundNumber % 100 == 0):
                print('q: ', len(self.queue), 'round:', roundNumber)

        urlMap, webGraph = self.makeGraph()
        storingTxt(('\n').join(urlMap), 'urlmap')
        storingTxt(('\n').join(webGraph), 'webgraph')


if __name__ == "__main__":
    WebGraph(
        startUrl=START_URL
    ).run()
