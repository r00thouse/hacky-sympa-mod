#!/usr/bin/python

import time
from configuration import loadConfiguration, settings
from sympa.subscribers import getSubscribers
from sympa.mod import HackyMod

def main():
    loadConfiguration('./settings.json')
    users = getSubscribers(settings['subscribersFile'])
    mod = HackyMod(users=users, listName=settings['listName'],
        sympaEmail=settings['sympaEmail'],
        moderatorEmail=settings['moderatorEmail'],
        moderatorPassword=settings['moderatorPassword'],
        imapSSLServer=settings['imapSSLServer'],
        imapSSLPort=settings['imapSSLPort'])

    while True:
        mod.moderate()
        # get emails, parse and moderate them every X minutes
        time.sleep(3)

if __name__ == '__main__':
    main()
