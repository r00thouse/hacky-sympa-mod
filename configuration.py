from sympa.utils import getFileContent
import json

settings = {
    'subscribersFile': './subscribers.json',
    'listName': None,
    'blacklistFile': './blacklist.txt',
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
    'getSubscribersMinutesInterval': 1440, # Retrieve subscribers each 24hrs
    'moderationMinutesInterval': 15 #
}

def loadConfiguration(filename):
    content = getFileContent(filename, parseJson=True)
    settingsKeys = settings.keys()

    for key in settingsKeys:
        if content.get(key):
            settings[key] = content[key]
