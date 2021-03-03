import re

FILE_NUMBER = ['01', '02', '03', '04', '06', '07', 18, 20, 21, 22, 23,
               24, 26, 28, 29, 31, 36, 38, 41, 42, 43, 44, 49]
WORDS = ['โควิด', 'วัคซีน', 'สถานการณ์', 'เศรษฐกิจ']


def openFile(fileNumber):
    fileName = str(fileNumber)+'.txt'
    f = open('./files/'+fileName, "r")
    return f


if (__name__ == '__main__'):
    for number in FILE_NUMBER:
        print('##########', number)

        for word in WORDS:
            file = openFile(number)
            count = 0

            for line in file:
                match = re.findall(word, line)
                count += len(match)

            file.close()
            print(word, ':', count)

        print()
