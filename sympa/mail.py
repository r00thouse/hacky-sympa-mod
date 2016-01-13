import imaplib
import email
import email.header

def sendEmail(to, subject, email, password, smtpServer, smtpPort):
    pass

"""
How to parse headers from raw email thanks to
https://gist.github.com/robulouski/7441883
Read IMAP4 RFC
"""
def getEmailsFromUser(fromEmail, userEmail, password, imapServer, imapPort):
    result = []
    print('Connecting to %s' % imapServer)
    M = imaplib.IMAP4_SSL(host=imapServer, port=imapPort)
    print('OK - Connected')

    print('Logging in as %s' % userEmail)
    rv, data = M.login(userEmail, password)
    if rv != 'OK':
        print('ERROR logging in')
        return

    print('OK - Logged in success')

    rv, data = M.select() # Selects default mailbox: inbox
    if rv != 'OK':
        print('ERROR getting default mailbox')
        return

    print('Searching for unseen emails from %s' % fromEmail)
    flags = '(UNSEEN FROM "%s")' % fromEmail
    rv, data = M.search(None, flags) # get emails with the unseen flag
    if rv != 'OK':
        pass
    print('Got this email identifiers: %s' % str(data[0]))

    for number in data[0].split():
        print('Fetching email %s' % number)
        rv, data = M.fetch(number, '(RFC822)')
        if rv != 'OK':
            pass

        # parsing email
        msg = email.message_from_string(data[0][1])
        subject = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(subject[0])
        sender = msg['From']
        content = ''
        if msg.is_multipart():
            print('Email is multipart, concatenating')
            content += concatenateMultipartEmail(msg.get_payload())
        else:
            content += msg.get_payload()

        content = content.decode('utf-8')
        if sender.find(fromEmail) != -1:
            print("""Subject: %s
                From: %s
                """ % (subject, sender))
            result.append({
                'subject': subject,
                'from': sender,
                'content': content
            })
    print('Logging out')
    M.logout()

    return result

def concatenateMultipartEmail(emailMessage):
    content = ''
    for payload in emailMessage:
        if payload.is_multipart():
            content += concatenateMultipartEmail(payload.get_payload())
        else:
            content += payload.get_payload()
    return content

def getModerationData(emailContent='', listName='', senderEmail=''):
    MODERATION_CODE_PATTERN = 'DISTRIBUTE %s' % listName

    senderEmail = ''
    index = emailContent.find(senderEmail)
    if index == -1:
        return None

    moderationCode = ''
    index  = emailContent.find(MODERATION_CODE_PATTERN)
    if index == -1:
        return None

    index += len(MODERATION_CODE_PATTERN) + 1
    while emailContent[index] != ' ' and emailContent[index] != '\r' and emailContent[index] != '\n':
        moderationCode += emailContent[index]
        index += 1

    return moderationCode
