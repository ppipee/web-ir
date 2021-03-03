from urlUtils import getDirectoryPath
from constants import BASE_PATH


def loadFileWithUrl(url):
    filePath = BASE_PATH + getDirectoryPath(url)
    rawHtml = ''

    try:
        rawHtml = loadFile(filePath)
    except:
        pass
        # print('load failed')

    return rawHtml


def loadFile(path):
    f = open(path, "r")
    data = f.read()
    f.close()

    return data
