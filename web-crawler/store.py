import os
import codecs
import re
from constants import BASE_PATH
from analyzer import getPath


def getDirectoryPath(url):
    path, _ = getPath(url)

    has_file_type = re.search('/.+\.html$', path)
    if(not has_file_type):
        path += '/index.html'

    words = ['http://', 'https://', 'https:', 'http:', 'www.', 'www3.']

    for word in words:
        path = path.replace(word, '')

    return path


def storing(data, file_name):
    f = codecs.open(file_name, 'w', 'utf-8')
    f.write(data)
    f.close()


def storingHtml(raw_html, path):
    success = False
    file_name = BASE_PATH + path
    print(file_name)

    lastParamIndex = file_name.rindex('/')
    folderName = file_name[:lastParamIndex]

    try:
        os.makedirs(folderName, 0o755, exist_ok=True)
        storing(raw_html, file_name)
        success = True
    except Exception as err:
        print(f'storing err: {err}',)

    return success


def storingTxt(data, file_name):
    storing(data, file_name+'.txt')
