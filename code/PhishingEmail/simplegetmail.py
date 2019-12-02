import imaplib

username = 'phishingdetective@gmail.com'
password = 'phishtooldetect97'
imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993

M = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
M.login(username, password)
M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message {0}\n{1}\n'.format(num, data[0][1]))
M.close()
M.logout()