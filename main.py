#!/usr/bin/python

import time
from threading import Thread
from logs import initLogs
from configuration import loadConfiguration, settings
from sympa.subscribers import getSubscribersFromFile, getSubscribersFromEmail
from sympa.subscribers import writeSubscribers
from sympa.mod import HackyMod

subscribedUsers = []
def getSubscribersAsync(usersReadyCallback):
    global subscribedUsers
    first = True

    backupSubscribedUsers = getSubscribersFromFile(settings['subscribersFile'])
    while True:
        print('[ASYNC] - Getting subscribed users...')
        subscribedUsers = getSubscribersFromEmail(
            listName=settings['listName'],
            sympaCommandEmail=settings['sympaCommandEmail'],
            listContactEmail=settings['listContactEmail'],
            moderatorEmail=settings['moderatorEmail'],
            moderatorPassword=settings['moderatorPassword'],
            imapServer=settings['imapSSLServer'], imapPort=settings['imapSSLPort'],
            smtpServer=settings['smtpServer'], smtpPort=settings['smtpPort'])

        print('[ASYNC] - Subscribed users fetched\n\n')
        if len(subscribedUsers) == 0:
            print('    [-] No subscribers fetched from email, using subscribers file')
            subscribedUsers = backupSubscribedUsers
        else:
            print('    [+] Writing new subscribers to file')
            writeSubscribers(settings['subscribersFile'], subscribedUsers)

        if first:
            first = False
            t = Thread(target=usersReadyCallback)
            t.start()

        print('[ASYNC] - Wating for next subscribed-users retrieval...')
        time.sleep(60*10)

def startModeration():
    global subscribedUsers
    mod = HackyMod(
        users=subscribedUsers,
        blacklistFile=settings['blacklistFile'],
        listName=settings['listName'],
        listContactEmail=settings['listContactEmail'],
        moderatorEmail=settings['moderatorEmail'],
        moderatorPassword=settings['moderatorPassword'],
        imapSSLServer=settings['imapSSLServer'],
        imapSSLPort=settings['imapSSLPort'],
        smtpServer=settings['smtpServer'],
        smtpPort=settings['smtpPort'])

    while True:
        print('\n')
        print('[MOD] - Starting moderation')
        mod.moderate()
        # get emails, parse and moderate them every X minutes
        time.sleep(60) # cada 2 minutos

def main():
    loadConfiguration('./settings.json')
    initLogs(settings['logFile'], debug=settings['debug'])

    t = Thread(target=getSubscribersAsync, args=(startModeration,))
    t.start()


if __name__ == '__main__':
    main()
