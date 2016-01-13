from sympa.utils import getFileContent
import json

settings = {
    'subscribersFile': './subscribers.json',
    'listName': None,
    'debug': False,
    'logFile': './hackymod.log',
    'listContactEmail': None,
    'sympaCommandEmail': None,
    'imapSSLServer': None,
    'imapSSLPort': None,
    'smtpServer': None,
    'smtpPort': None,
    'moderatorEmail': None,
    'moderatorPassword': None,
}

def loadConfiguration(filename):
    content = getFileContent(filename, parseJson=True)
    settingsKeys = settings.keys()

    for key in settingsKeys:
        if content.get(key):
            settings[key] = content[key]
