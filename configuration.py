from simpa.utils import getFileContent
import json

settings = {
    'subscribersFile': './subscribers.json',
    'logFile': './hackymod.log',
    'simpaEmail': None,
    'imapSSLServer': None,
    'imapSSLPort': None,
    'moderatorEmail': None,
    'moderatorPassword': None,
}

def loadConfiguration(filename):
    content = getFileContent(filename, parseJson=True)
    settingsKeys = settings.keys()

    for key in settingsKeys:
        if content.has_key(key):
            settings[key] = content[key]
