#!/usr/bin/python

from configuration import loadConfiguration, settings
from simpa.subscribers import getSubscribers

def main():
    loadConfiguration('./settings.json')
    users = getSubscribers(settings['subscribersFile'])



if __name__ == '__main__':
    main()
