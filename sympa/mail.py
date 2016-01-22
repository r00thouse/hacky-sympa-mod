import imaplib
import smtplib
import email
import email.header


def sendEmail(to, subject, emailUser, password, smtpServer, smtpPort):
    try:
        message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (emailUser, to, subject, '')
        smtpClient = smtplib.SMTP(smtpServer, smtpPort)
        smtpClient.ehlo()
        smtpClient.starttls()
        smtpClient.ehlo()
        smtpClient.login(emailUser, password)
        smtpClient.sendmail(emailUser,to,message)
        smtpClient.close()
    except Exception as e:
        print('[EMAIL] - Failed to send email to %s from %s, server %s' % (to, emailUser, smtpServer))
        print('[EMAIL] - Error: %s' % str(e))
        return False

    return True

"""
How to parse headers from raw email thanks to
https://gist.github.com/robulouski/7441883
Read IMAP4 RFC
"""
def getEmailsFromUser(fromEmail, userEmail, password, imapServer, imapPort, listname, subjectFilter=''):
    result = []
    print('[EMAIL] - Connecting to %s' % imapServer)
    M = imaplib.IMAP4_SSL(host=imapServer, port=imapPort)
    print('    [+] OK - Connected')

    print('[EMAIL] - Logging in as %s' % userEmail)
    rv, data = M.login(userEmail, password)
    if rv != 'OK':
        print('    [-] ERROR logging in')
        return

    print('    [+] OK - Logged in success')

    rv, data = M.select() # Selects default mailbox: inbox
    if rv != 'OK':
        print('    [-] ERROR getting default mailbox')
        return

    flags = '(UNSEEN FROM "%s"' % fromEmail

    if len(subjectFilter) > 0:
        flags = flags + ' SUBJECT "%s"' % subjectFilter
    else:
        flags = flags + ' NOT SUBJECT "REVIEW %s"' % listname
    flags += ')'

    print('[EMAIL] - Searching for unseen emails from %s, %s' % (fromEmail, flags))
    rv, data = M.search(None, flags) # get emails with the unseen flag
    if rv != 'OK':
        pass
    print('[EMAIL] - Got this email identifiers: %s' % str(data[0]))

    for number in data[0].split():
        print('[EMAIL] - Fetching email %s' % number)
        rv, data = M.fetch(number, '(RFC822)')
        if rv != 'OK':
            pass

        # parsing email
        msg = email.message_from_string(data[0][1])
        subject = email.header.decode_header(msg['Subject'])[0]
        subject = subject[0]
        sender = msg['From']
        content = ''
        if msg.is_multipart():
            print('    [+] Email is multipart, concatenating')
            content += concatenateMultipartEmail(msg.get_payload())
        else:
            content += msg.get_payload()


        print('\n\n')
        print('    [+] Subject: %s' % subject)
        print('    [+] From: %s' % sender)

        content = content.decode('utf-8')

        if not sender or not subject:
            return []

        if sender.find(fromEmail) != -1:

            result.append({
                'subject': subject,
                'from': sender,
                'content': content
            })
    print('[EMAIL] - Logging out')
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

    # print('######################################')
    # print('##### Message body from %s ######' % senderEmail)
    # print(' %s ' % emailContent)
    # print('###### END OF BODY####################')

    MODERATION_CODE_PATTERN = 'DISTRIBUTE %s' % listName

    senderEmail = ''
    index = emailContent.find(senderEmail)
    if index == -1:
        print '[MOD] - Not found sender email %s' % senderEmail
        return None

    moderationCode = ''
    index  = emailContent.find(MODERATION_CODE_PATTERN)
    if index == -1:
        print '[MOD] - Not found moderation code'
        return None

    index += len(MODERATION_CODE_PATTERN) + 1
    while emailContent[index] != ' ' and emailContent[index] != '\r' and emailContent[index] != '\n':
        moderationCode += emailContent[index]
        index += 1

    return moderationCode
