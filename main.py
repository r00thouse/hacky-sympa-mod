#!/usr/bin/python

import time
from logs import initLogs
from configuration import loadConfiguration, settings
from sympa.subscribers import getSubscribers
from sympa.mod import HackyMod

def main():
    loadConfiguration('./settings.json')
    initLogs(settings['logFile'], debug=settings['debug'])

    users = getSubscribers(settings['subscribersFile'])
    mod = HackyMod(users=users,
        blacklist=[],
        listName=settings['listName'],
        listContactEmail=settings['listContactEmail'],
        moderatorEmail=settings['moderatorEmail'],
        moderatorPassword=settings['moderatorPassword'],
        imapSSLServer=settings['imapSSLServer'],
        imapSSLPort=settings['imapSSLPort'],
        smtpServer=settings['smtpServer'],
        smtpPort=settings['smtpPort'])

    while True:
        print('Starting moderation')
        mod.moderate()
        # get emails, parse and moderate them every X minutes
        time.sleep(3)

if __name__ == '__main__':
    main()
