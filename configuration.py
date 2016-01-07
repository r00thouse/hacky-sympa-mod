from simpa.utils import getFileContent
import json

settings = {
    'subscribersFile': './subscribers.json',
    'logFile': './hackymod.log',
    'moderatorEmail': None,
    'moderatorPassword': None,
}

def loadConfiguration(filename):
    content = getFileContent(filename, parseJson=True)
    if content.has_key('subscribersFile'):
        settings['subscribersFile'] = content['subscribersFile']
    if content.has_key('logFile'):
        settings['logFile'] = content['logFile']
    if content.has_key('moderatorEmail'):
        settings['moderatorEmail'] = content['moderatorEmail']
    if content.has_key('moderatorPassword'):
        settings['moderatorPassword'] = content['moderatorPassword']

