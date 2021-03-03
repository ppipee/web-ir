import codecs


def storing(data, file_name):
    f = codecs.open(file_name, 'w', 'utf-8')
    f.write(data)
    f.close()


def storingTxt(data, file_name):
    storing(data, file_name+'.txt')
