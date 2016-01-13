import re
from .mail import getEmailsFromUser, getModerationData, sendEmail

EMAIL_SIMPLE_REGEX = '[\w\.-]+@[\w\.-]+'

class HackyMod:
    def __init__(self, listName='', users=[], blacklistFile=[], listContactEmail=None,
            moderatorEmail=None, moderatorPassword=None, imapSSLServer=None,
            imapSSLPort=993, smtpServer=None, smtpPort=0):
        self.listName = listName
        self.users = users
        self.blacklistFile = blacklistFile
        self.listContactEmail = listContactEmail
        self.moderatorEmail = moderatorEmail
        self.moderatorPassword = moderatorPassword
        self.imapSSLServer = imapSSLServer
        self.imapSSLPort = imapSSLPort
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort

    def __parseEmailFromSubject(self, subject):
        results = re.findall(EMAIL_SIMPLE_REGEX, subject)
        if len(results) > 0:
            return results[0]
        return None

    def __isUserSubscriberd(self, email):
        users = self.users
        for usr in users:
            if usr['email'] == email:
                return True
        return False

    def __isUserInBlackList(self, email):
        #blacklist = self.blacklist
        # Added a blacklist file (testing)
        blf = open(self.blacklistFile, 'r')
        blacklist = blf.reeadlines()

        for usr in blacklist:
            if usr == email:
                return True
        return False

    def __isGoodUser(self, email):
        return self.__isUserSubscriberd(email) and not self.__isUserInBlackList(email)

    def moderate(self):
        emails = getEmailsFromUser(self.listContactEmail, self.moderatorEmail,
            self.moderatorPassword, self.imapSSLServer, self.imapSSLPort)

        for email in emails:
            senderEmail = self.__parseEmailFromSubject(email['subject'])
            if not senderEmail:
                print('Invalid email subject')
                continue

            print('Moderating message from %s' % senderEmail)

            moderationCode = getModerationData(email['content'], self.listName, senderEmail)
            if not moderationCode:
                print('Email with invalid format')
                continue

            print('Email has moderation code %s' % moderationCode)
            if self.__isGoodUser(senderEmail):
                print('%s is not on the blacklist :D, distributing.' % senderEmail)
                subject = 'DISTRIBUTE % s %s' % (self.listName, moderationCode)
                # sendEmail(self.sympaDistributeEmail, subject)
            else:
                print('%s is not a good user the message has to be moderated manually' % senderEmail)

