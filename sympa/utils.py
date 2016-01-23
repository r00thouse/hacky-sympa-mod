import json

def arrayToFile(filename, array=[]):
    fd = open(filename, 'w')
    for item in array:
        fd.write(item + '\n')
    fd.close()

def getFileContent(filename, parseJson=False):
    fd = open(filename, 'r')
    content = fd.read()
    fd.close()

    if parseJson:
        content = json.loads(content)

    return content

def removeEOLCharacters(item, replace=''):
    item = item.replace('\n', replace)
    item = item.replace('\r', replace)

    return item

def getFileLines(filename, removeEOL=False):
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()

    if removeEOL:
        lines = [removeEOLCharacters(line) for line in lines]

    return lines

def hasBadKeywords(emailContent):
    keywords = [
        'puta', 'mierda', 'carajo', 'cerdos', 'cerdo', 'trasero',
        'mother fuckers', 'fuck', 'bitch', 'bozal', 'bosal', 'pene', 'vagina',
        'marica', 'maricon', 'gay', 'lesbiana', 'gordo', 'puerco', 'puercos',
        'franchute', 'maldit', 'cojud', 'huevon', 'boludo',
        'huev', 'shit', 'asshole'
    ]
