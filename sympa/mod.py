import re
from .mail import getEmailsFromUser, getModerationData, sendEmail
from .utils import getFileLines

EMAIL_SIMPLE_REGEX = '[\w\.-]+@[\w\.-]+'

class HackyMod:
    def __init__(self,
            listName='', users=[], sympaCommandEmail='',
            blacklistFile=[], listContactEmail=None,
            moderatorEmail=None, moderatorPassword=None, imapSSLServer=None,
            imapSSLPort=993, smtpServer=None, smtpPort=0):
        self.listName = listName
        self.users = users
        self.sympaCommandEmail = sympaCommandEmail
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

    def __isUserSubscribed(self, email):
        users = self.users
        # print('Compring %s with subscribed users' % email)
        for usr in users:
            if usr == email:
                return True
        return False

    def __isUserInBlackList(self, email):
        # Added a blacklist file (testing)
        blacklist = getFileLines(self.blacklistFile, removeEOL=True)

        for usr in blacklist:
            if usr == email:
                return True
        return False

    def __isGoodUser(self, email):
        isSubscribed = self.__isUserSubscribed(email)
        isInBlackList = self.__isUserInBlackList(email)

        print('    [+] %s is subscribed: %s' % (email, isSubscribed))
        print('    [+] %s is in black list: %s' % (email, isInBlackList))

        return isSubscribed and not isInBlackList

    def moderate(self):
        emails = getEmailsFromUser(self.listContactEmail, self.moderatorEmail,
            self.moderatorPassword, self.imapSSLServer, self.imapSSLPort, self.listName)

        for email in emails:
            senderEmail = self.__parseEmailFromSubject(email['subject'])
            if not senderEmail:
                print('[MOD] - Invalid email subject')
                continue

            print('[MOD] - Moderating message from %s' % senderEmail)

            moderationCode = getModerationData(email['content'], self.listName, senderEmail)
            if not moderationCode:
                print('    [+] Email with invalid format')
                continue

            print('    [+] Email has moderation code %s' % moderationCode)

            if self.__isGoodUser(senderEmail):
                print('    [+] %s is a good user :D, distributing.' % senderEmail)
                subject = 'DISTRIBUTE % s %s' % (self.listName, moderationCode)
                # sendEmail(self.sympaDistributeEmail, subject)
                attempts = 1
                while True:
                    sent = sendEmail(self.sympaCommandEmail, subject,
                        self.moderatorEmail, self.moderatorPassword,
                        self.smtpServer, self.smtpPort)
                    if sent:
                        print('[MOD] - Email distributed successfully')
                        break
                    attempts += 1
                    if attempts == 10:
                        break
            else:
                print('    [-] %s is not a good user the message has to be moderated manually' % senderEmail)
