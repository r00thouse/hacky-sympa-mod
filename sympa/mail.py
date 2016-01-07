import imaplib
import email
import email.header

"""
TODO:
make a method to get all emails from an email (the riseup email
that most of the time will be r00thouse-request@lists.riseup.net)
analize the format of this email:

One new message for list r00thouse from serguimant@openmailbox.org arrived.

5 messages are awaiting moderation.
To view the messages, please click on the following URL:
<https://lists.riseup.net/www/ticket/18326481916985>

To distribute the attached message in list r00thouse:
<mailto:sympa@lists.riseup.net?subject=DISTRIBUTE%20r00thouse%20227d40889a2c5af57ee4a6541f9e4191>
Or send a message to sympa@lists.riseup.net with the following subject:
DISTRIBUTE r00thouse 227d40889a2c5af57ee4a6541f9e4191

To reject it (it will be removed):
<mailto:sympa@lists.riseup.net?subject=REJECT%20r00thouse%20227d40889a2c5af57ee4a6541f9e4191>
Or send a message to sympa@lists.riseup.net with the following subject:
REJECT r00thouse 227d40889a2c5af57ee4a6541f9e4191

KEY PARTS
list <listName> from <email> arrived

DISTRIBUTE <listName> <someCode>

So if <email> is subscribed and it's not in the black list
send an email to sympa@lists.riseup.net with the given subject
DISTRIBUTE <listName> <someCode>
that will distribute <email>'s message to the whole list
"""

print 'connecting...'
M = imaplib.IMAP4_SSL(host='imap.openmailbox.org')
print 'loggin in'
M.login('carlitosfoobar@openmailbox.org', 'carlitospassword')


print 'SELECT'
rv, data = M.select()
print rv, data

print 'SEARCH'
rv, data = M.search(None, 'UNSEEN')
print rv, data

print 'reading emails...'
for number in data[0].split():
    print 'FETCH %s' % number
    # gets the full message
    rv, data = M.fetch(number, '(RFC822)')
    print rv

    print 'parsing email'
    msg = email.message_from_string(data[0][1])

    subject = email.header.decode_header(msg['Subject'])[0]
    subject = unicode(subject[0])
    print 'Subject:', subject
    print 'From:', msg['From']
    print 'Content:'
    if msg.is_multipart():
        print 'it is multipart'
        for payload in msg.get_payload():
            print payload.get_payload()
    else:
        print msg.get_payload()

print 'loggin out'
M.logout()

print 'done'
