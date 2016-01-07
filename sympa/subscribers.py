from utils import getFileContent

def getSubscribers(filename):
    subscriberList = getFileContent(filename, parseJson=True)

    return subscriberList
