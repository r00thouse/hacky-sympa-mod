import time
import re
from utils import getFileLines, removeEOLCharacters, arrayToFile
from mail import getEmailsFromUser
from mail import sendEmail

def writeSubscribers(filename, subscribers):
    arrayToFile(filename, subscribers)

def getSubscribersFromFile(filename):
    subscriberList = getFileLines(filename, removeEOL=True)

    return subscriberList

"""
Get subscribers by sending the command REVIEW
REVIEW listName
"""
def getSubscribersFromEmail(**kargs):
    listName = kargs['listName']
    sympaCommandEmail = kargs['sympaCommandEmail']
    listContactEmail = kargs['listContactEmail']
    moderatorEmail = kargs['moderatorEmail']
    moderatorPassword = kargs['moderatorPassword']
    imapServer = kargs['imapServer']
    imapPort = kargs['imapPort']
    smtpServer = kargs['smtpServer']
    smtpPort = kargs['smtpPort']

    command = 'REVIEW %s' % listName
    sendAttempts = 1
    while True:
        print('[SUBSCRIBED USERS] - Sending a subscribers request to %s' % sympaCommandEmail)
        wasEmailSent = sendEmail(sympaCommandEmail, command, moderatorEmail, moderatorPassword,
            smtpServer, smtpPort)
        if wasEmailSent:
            break

        sendAttempts += 1
        if sendAttempts == 10:
            return []

    print('[SUBSCRIBED USERS] - email sent')
    time.sleep(30)

    print('[SUBSCRIBED USERS] - reading email content...')
    emails = getEmailsFromUser(listContactEmail, moderatorEmail, moderatorPassword,
        imapServer, imapPort, listName, subjectFilter='REVIEW r00thouse')

    EMAIL_SIMPLE_REGEX = '[\w\.-]+@[\w\.-]+'

    subscribedUsers = []
    for message in emails:
        content = message['content']
        content = removeEOLCharacters(content, replace=' ')
        regexResult = re.findall(EMAIL_SIMPLE_REGEX, content)

        for subsUser in regexResult:
            subscribedUsers.append(subsUser)

    return subscribedUsers

# def foobar():
    # getSubscribers2(listName='r00thouse', sympaCommandEmail='sympa@lists.riseup.net',
        # listContactEmail='r00thouse-request@lists.riseup.net',
        # moderatorEmail='roggs@openmailbox.org', moderatorPassword='5rogggggs50',
        # imapServer='imap.openmailbox.org', imapPort=993,
        # smtpServer='smtp.openmailbox.org', smtpPort=587)
