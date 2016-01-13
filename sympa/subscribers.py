import time
from utils import getFileContent
from .mail import getEmailsFromUser
from .mail import sendEmail

def getSubscribers(filename):
    subscriberList = getFileContent(filename, parseJson=True)

    return subscriberList

"""
Get subscribers by sending the command REVIEW
REVIEW listName
"""
def getSubscribers2(**kargs):
    subscribersFile = kargs['subscribersFile']
    listName = kargs['listName']
    sympaCommandEmail = kargs['sympaCommandEmail']
    moderatorEmail = kargs['moderatorEmail']
    password = kargs['moderatorPassword']
    imapServer = kargs['imapServer']
    imapPort = kargs['imapPort']
    smtpServer = kargs['smtpServer']
    smtpPort = kargs['smtpPort']

    command = 'REVIEW %s' % listName
    print('Sending a subscribers request to %s' % sympaCommandEmail)
    # sendEmail(sympaCommandEmail, command, moderatorEmail, moderatorPassword,
    #     smtpServer, smtpPort)

    time.sleep('10')

    # emails = getEmailsFromUser(sympaCommandEmail, userEmail, password, imapServer, imapPort)

    return []
