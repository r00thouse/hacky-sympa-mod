from mail import getEmailsFromUser, getModerationData, sendEmail

class HackyMod:
    def __init__(self, listName='', users=[], sympaEmail=None, moderatorEmail=None,
                moderatorPassword=None, imapSSLServer=None, imapSSLPort=993):
        self.listName = listName
        self.users = users
        self.sympaEmail = sympaEmail
        self.moderatorEmail = moderatorEmail
        self.moderatorPassword = moderatorPassword
        self.imapSSLServer = imapSSLServer
        self.imapSSLPort = imapSSLPort

    def __isGoodUser(self, email):
        users = self.users
        for usr in users:
            if usr['email'] == email:
                if !usr['moderated']:
                    return True
                return False
        return False

    def moderate(self):
        emails = getEmailsFromUser(self.sympaEmail, self.moderatorEmail,
            self.moderatorPassword, self.imapSSLServer, self.imapSSLPort)

        for email in emails:
            senderEmail, moderationCode = getModerationData(email, self.listName)
            if self.__isGoodUser(senderEmail):
                subject = 'DISTRIBUTE % s %s' % (self.listName, moderationCode)
                # sendEmail(self.sympaDistributeEmail, subject)

