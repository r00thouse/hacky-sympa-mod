import imaplib
import email
import email.header


"""
TODO:
make a method to get all
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
