import time
from itertools import chain
import email
import imaplib
import pprint as pp

import argparse


# get commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--password')
parser.add_argument('-u', '--username')
args = parser.parse_args()

print("Command line arguments:");print(args);print(78*'-')


imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993
username = 'phishingdetective@gmail.com'
password = 'phishtooldetect97'

# Restrict mail search. Be very specific.
# Machine should be very selective to receive messages.
criteria = {
  # 'FROM':    'isaacpitblado@tamu.edu',
  # 'SUBJECT': 'PHISHING',
  # 'BODY':    'SECRET SIGNATURE',
}
uid_max = 0


def search_string(uid_max, criteria):
  c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
  return '(%s)' % ' '.join(chain(*c))
  # Produce search string in IMAP format:
  #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)


def get_first_text_block(msg):
  type = msg.get_content_maintype()

  if type == 'multipart':
    for part in msg.get_payload():
      if part.get_content_maintype() == 'text':
        return part.get_payload()
  elif type == 'text':
    return msg.get_payload()


server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select('INBOX')

# result, data = server.uid('search', None, search_string(uid_max, criteria))
result, data = server.search(None, 'ALL')

uids = [int(s) for s in data[0].split()]
# print("original uids: ", uids)
if uids:
  uid_max = max(uids)
  # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

server.logout()


# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.
while 1:
  # Have to login/logout each time because that's the only way to get fresh results.

  server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
  server.login(username, password)
  server.select('INBOX')

  # result, data = server.uid('search', None, search_string(uid_max, criteria))
  result, data = server.search(None, 'ALL')

  uids = [int(s) for s in data[0].split()]
  # print('UID: ', uids)
  # for uid in uids:
  for i in range(len(uids) -1, len(uids) - 2, -1):
    # Have to check again because Gmail sometimes does not obey UID criterion.
    uid = uids[i]
    # if uid > uid_max:
    if True:
      print("uid: ", uid)
      result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
      # print("res: ", result)
      # print("data: ", data)
      # print("data:")
      # pp.pprint(data)
      


      for response_part in data:
        if isinstance(response_part, tuple):
          # print("response_part: ", response_part)
          # print("response_part[1]: ", response_part[1])
          msg = email.message_from_string(response_part[1].decode('utf-8'))
          print('msg_keys: ');pp.pprint(msg.keys())
          print("msg: \n", msg)
          
          email_subject = msg['subject']
          email_from = msg['from']
          email_payload = msg.get_payload(decode=True)
          print('From : ' + email_from + '\n')
          print('Subject : ' + email_subject + '\n')
          print('Payload :')
          print(email_payload)
          print('Content-type', msg['Content-type'])
          print('Mime-Version', msg['Mime-Version'])
          print("is multi part: ", msg.is_multipart())
          if msg.is_multipart():
            for payload in msg.get_payload():
              print('To:\t\t', msg['To'])
              print('From:\t',     msg['From'])
              print('Subject:', msg['Subject'])
              print('Date:\t',msg['Date'])
              for part in msg.walk():
                print("*" * 78)
                print("part.content_type: {0}".format(part.get_content_type()))
                # if (part.get_content_type() == 'text/plain') and (part.get('Content-Disposition') is None):
                print('Body:\t',part.get_payload())
              
              
              # break


          # for part in msg.walk():
          #   print("part: ", part)
            
          
          

      
      # msg = email.message_from_string(data[0][1])
      
      # uid_max = uid
    
      # text = get_first_text_block(msg)
      # print('New message :::::::::::::::::::::')
      # print(text)

  server.logout()
  break
  time.sleep(1)
