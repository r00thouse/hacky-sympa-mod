#!/usr/bin/python

import time
from configuration import loadConfiguration, settings
from simpa.subscribers import getSubscribers
from simpa.mod import HackyMod

def main():
    loadConfiguration('./settings.json')
    users = getSubscribers(settings['subscribersFile'])
    mod = HackyMod(users=users, simpaEmail=settings['simpaEmail'],
        moderatorEmail=settings['moderatorEmail'],
        moderatorPassword=settings['moderatorPassword'])

    while True:
        mod.moderate()
        # get emails, parse and moderate them every X minutes
        time.sleep(3)

if __name__ == '__main__':
    main()
