import codecs
import numpy as np

BASE_PATH = '/home/ppipee/Desktop/CPE/web-ir/assignment/assignment-4/'
ALPHA = 0.85
SIGMA = 10**-15


def loadGraph():
    path = BASE_PATH + 'webgraph.txt'
    f = open(path, "r")
    data = f.read()
    f.close()

    return data


def storeScore(scores):
    scores = [str(score) for score in scores]
    f = codecs.open('page_scores.txt', 'w', 'utf-8')
    f.write('\n'.join(scores))
    f.close()


def initGraph(raw):
    webGraph = raw.split('\n')

    for i, row in enumerate(webGraph):
        webGraph[i] = row.split(', ')

    return webGraph


class PageRankComputation:
    def __init__(self, alpha, sigma, webGraph):
        self.alpha = alpha
        self.sigma = sigma
        self.webGraph = webGraph
        self.size = len(webGraph)
        self.rankScore = np.array([1/self.size for _ in range(self.size)])
        self.solveLeakProblem()
        self.pageRank = np.array(self.initPageRank())

    def solveLeakProblem(self):
        for row, nodes in enumerate(self.webGraph):
            if(nodes[0] == '-'):
                self.webGraph[row] = [i+1 for i in range(self.size)]

    def initPageRank(self):
        pageRank = []
        defaultNodes = [0 for _ in range(self.size)]
        for webGraphNodes in self.webGraph:
            row = defaultNodes[:]
            defaultScore = 1/len(webGraphNodes)

            for node in webGraphNodes:
                nodeIndex = int(node)-1
                row[nodeIndex] = defaultScore

            pageRank.append(row)

        return pageRank

    def computeRankScore(self):
        rankScore = self.alpha * np.matmul(np.transpose(self.pageRank), self.rankScore) + (
            1-self.alpha)*np.array([1/self.size for _ in range(self.size)])

        return rankScore

    def getRankValue(self, rankScore):
        value = 0
        for score in rankScore:
            value += score

        return value

    def compute(self):
        round = 1
        # storeScore(self.pageRank)
        # rankScore = self.computeRankScore()

        # value = self.getRankValue(rankScore)
        # print(value)
        while True:
            # for i in range(100):
            rankScore = self.computeRankScore()

            prevRankValue = self.getRankValue(self.rankScore)
            currentRankValue = self.getRankValue(rankScore)

            print(round, 'diff', prevRankValue -
                  currentRankValue, currentRankValue)
            if(abs(prevRankValue-currentRankValue) < self.sigma):
                break

            round += 1
            self.rankScore = rankScore

        print('sum score :', self.getRankValue(self.rankScore))
        return self.rankScore


if __name__ == "__main__":
    rawFile = loadGraph()
    webGraph = initGraph(rawFile)

    rankScore = PageRankComputation(
        alpha=ALPHA,
        sigma=SIGMA,
        webGraph=webGraph
    ).compute()

    storeScore(rankScore)
