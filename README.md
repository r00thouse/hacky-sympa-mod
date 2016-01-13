Hacky Sympa Mod
===============

##Create settings files

In order to create a default settings-file execute:

    $ ./init.sh

##Settings

The settings values that need to be set on settings.json file are:

* subscribersFile (string) - It's the filename where subscribed users will remain
* debug (boolean) - Wheter or not logs will be displayed on stdout or a logfile
* logFile (string) - Where logs will be stored
* listName (string) - Listname to moderate
* listContactEmail (email) - Email address that sends messages for moderation, it's commonly  [listName]-request@lists.riseup.net
* sympaCommandEmail (email) - Email address where commands will be sent, it is used to get subscribed users
* moderatorEmail (email) - Email address that has owner roles on a riseup list
* moderatorPassword (string) - Moderator password
* imapSSLServer (string) - In order to fetch emails, it's necessary to connect to the moderator's email provider IMAP server
* imapSSLPort (integer) - IMAP server port
* smptServer (string) - In order to send emails, it's necessary to connect to the moderator's email provider SMTP server
* smtpPort (integer) - SMTP server port
* blacklistFile (string) - Name of the text file containing emails in the black list (one email per line)

##How it works

The script works the like this:

* It connects to SMTP server
* With a moderator account, it sends a REVIEW message to [sympaCommandEmail]
* Then it reads the response to that command requests and gets all subscribed users
* It connects to IMAP server and logs in with a modertor account
* Fetch unseen emails from [listContactEmail]
* For all fetched emails the script gets a moderation unique code and a sender email
* If the sender email is subscribed and it's not in the black list
** The scripts sends a DISTRIBUTE [moderation-unique-code] [listName] command via SMTP to [sympaCommandEmail]
* If the sender email is not subscribed or it's in the black list
** The script leaves that message for manual moderation


##Important note
The riseup list has to send all messages for moderation.
