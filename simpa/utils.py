import json

def getFileContent(filename, parseJson=False):
    fd = open(filename, 'r')
    content = fd.read()
    fd.close()

    if parseJson:
        content = json.loads(content)

    return content
