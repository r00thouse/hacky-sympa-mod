import json

def getFileContent(filename, parseJson=False):
    fd = open(filename, 'r')
    content = fd.read()
    fd.close()

    if parseJson:
        content = json.loads(content)

    return content

def __removeEOL(item):
    item = item.replace('\n', '')
    item = item.replace('\r', '')

    return item

def getFileLines(filename, removeEOL=False):
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()

    if removeEOL:
        lines = [__removeEOL(line) for line in lines]

    return lines
