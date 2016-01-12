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

    M = imaplib.IMAP4_SSL(host=imapServer, port=imapPort)
    rv, data = M.login(userEmail, password)
    if rv != 'OK':
        pass # handle error

    rv, data = M.select() # Selects default mailbox: inbox
    if rv != 'OK':
        pass

    rv, data = M.search(None, 'UNSEEN') # get emails with the unseen flag
    if rv != 'OK':
        pass

    for number in data[0].split():
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
            for payload in msg.get_payload():
                content += payload.get_payload()
                content += '\n'
        else:
            content = msg.get_payload()

        if sender.find(fromEmail) != -1:
            result.append({
                'subject': subject,
                'from': sender,
                'content': content
            })
    M.logout()

    return result

def getModerationData(emailContent='', listName=''):
    pattern1 = 'list %s from' % listName
    pattern2 = 'DISTRIBUTE %s' % listName

    senderEmail = ''
    index = emailContent.find(pattern1)
    if index == -1:
        pass # throw error of invalid format

    index += len(pattern1) + 1
    while emailContent[index] != ' ' || emailContent[index] != '\r' || emailContent[index] != '\n':
        senderEmail += emailContent[index]
        index += 1

    moderationCode = ''
    index  = emailContent.find(pattern2)
    if index == -1:
        pass # throw error of invalid format

    index += len(pattern2) + 1
    while emailContent[index] != ' ' || emailContent[index] != '\r' || emailContent[index] != '\n':
        moderationCode += emailContent[index]
        index += 1

    return senderEmail, moderationCode
