#!/usr/bin/env python
 
"""MailBox class for processing IMAP email.
 
(To use with Gmail: enable IMAP access in your Google account settings)
 
usage with GMail:
 
    import mailbox
 
    with mailbox.MailBox(gmail_username, gmail_password) as mbox:
        print mbox.get_count()
        print mbox.print_msgs()
 
 
for other IMAP servers, adjust settings as necessary.    
"""
 
 
import imaplib
import time
import uuid
import os
from email import email
from read_cimis_csv import *
from spacial_csv  import *
from spacial_xml   import *
 
 
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = '993'
IMAP_USE_SSL = True
 

 
 
class MailBox(object):
    
    def __init__(self, user, password):
        self.user = user
        self.password = password
        if IMAP_USE_SSL:
            self.imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        else:
            self.imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
 
    def __enter__(self):
        self.imap.login(self.user, self.password)
        return self
 
    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()
 
    def close( self ):
       self.imap.close()

    def get_count(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        return sum(1 for num in data[0].split())
 
    def fetch_message(self, num):
        self.imap.select('Inbox')
        status, data = self.imap.fetch(str(num), '(RFC822)')
        email_msg = email.message_from_string(data[0][1])
        return email_msg
 
    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
 
    def delete_all(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in data[0].split():
            self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
 
    def process_msgs(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            #print 'Message %s\n%s\n' % (num, data[0][1])
  
            for response_part in data:
               if isinstance(response_part, tuple):
                  msg = email.message_from_string(response_part[1])
                  varSubject = msg['subject']
                  varFrom = msg['from']
                  #remove the brackets around the sender email address
                  varFrom = varFrom.replace('<', '')
                  varFrom = varFrom.replace('>', '')
                 
                  body = ""
                  for part in msg.walk():
###                     if part.get_content_type() == "text/plain": # ignore attachments / html
###                        body = body + part.get_payload(decode=True)

                        # is this part an attachment ?
                        if part.get('Content-Disposition') is None:
                         continue
                        filename = part.get_filename()
                        print("filename",filename)
                        counter = 1
                        # if there is no filename, we create one with a counter to avoid duplicates
                        if not filename:
                           filename = 'part-%03d%s' % (counter, 'bin')
                           counter += 1
                        file_list = filename.split('/')
                        file_list_len = len(file_list)
                        filename = file_list[file_list_len-1]

                        att_path = "email_data/"+filename
                        #Check if its already there
                        if not os.path.isfile(att_path) :
                          #print("writing file")
                          # finally write the stuff
                          fp = open(att_path, 'wb')
                          fp.write(part.get_payload(decode=True))
                          fp.close()               
                        #process_input_message( varFrom,varSubject,body)
                        process_downloaded_messages()




    def get_latest_email_sent_to(self, email_address, timeout=300, poll=1):
        start_time = time.time()
        while ((time.time() - start_time) < timeout):
            # It's no use continuing until we've successfully selected
            # the inbox. And if we don't select it on each iteration
            # before searching, we get intermittent failures.
            status, data = self.imap.select('Inbox')
            if status != 'OK':
                time.sleep(poll)
                continue
            status, data = self.imap.search(None, 'TO', email_address)
            data = [d for d in data if d is not None]
            if status == 'OK' and data:
                for num in reversed(data[0].split()):
                    status, data = self.imap.fetch(num, '(RFC822)')
                    email_msg = email.message_from_string(data[0][1])
                    return email_msg
            time.sleep(poll)
        raise AssertionError("No email sent to '%s' found in inbox "
             "after polling for %s seconds." % (email_address, timeout))
 
    def delete_msgs_sent_to(self, email_address):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'TO', email_address)
        if status == 'OK':
            for num in reversed(data[0].split()):
                status, data = self.imap.fetch(num, '(RFC822)')
                self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
       


def look_for_spacial_data():
    
     global eto
     global prep
     if eto[1] != .5:
       return 

     os.chdir("email_data")
     try:
        files = glob.glob("C*.csv")  # get a list of files that match spatial cimis files
        if len(files) == 0:
           os.chdir("../")
           return 0
        for i in files:
           lines   = open(i).readlines()
           keys    = (lines[0].strip()).split(",")
           values = (lines[1].strip()).split(",")
           print keys[0].strip()
           if keys[0].strip() == "Address":
             print "values ->",values
             eto[1] = float(values[7]) - prep
             break

        
     
     except:
       pass
  
     os.chdir("../" ) #return back to parnent dir
   

def look_for_eto_data():
     global eto
     global prep
     if eto[0] != 0:
       return 
     os.chdir("email_data")
     try:
        files = glob.glob("C*.csv")  # get a list of files that match spatial cimis files
        if len(files) == 0:
           os.chdir("../")
      
        
       
        for i in files:
         
           lines   = open(i).readlines()
           keys    = (lines[0].strip()).split(",")
           values = (lines[1].strip()).split(",")
           if keys[0].strip() == "Stn Id":
             
             eto[0] = float(values[5]) - float( values[7] )
             #print "x----------",eto[0],float(values[7])
             prep = float( values[7])
             break

    
     
     except:
       pass
     os.chdir("../" ) #return back to parnent dir
     


def process_downloaded_messages():
   look_for_eto_data() 
   look_for_spacial_data() 
   os.system( "rm email_data/*")




#def process_downloaded_messages():
#    print "process downloaded messages"
#    x = Station_Cimis()
#    cimis_data = x.get_cimis_data()
#    print "cimis_data",cimis_data
#    cimis_eto = float(cimis_data["evap"]) - float(cimis_data["precp"] )
#    print "starting spatial"
#    x = Spatial_Cimis()
#    spacial_eto = x.get_cimis_data()
#    if spacial_eto == 0:
#       print "starting spatial eto xml"
#       x = Spatial_Cimis_XML()
#       spacial_eto = x.get_cimis_data()
#    spacial_eto = float(spacial_eto) - float(cimis_data["precp"] )
#    return [ cimis_eto, spacial_eto ]  
    
eto = []
prep = 0

def process_cimis_data( imap_username, imap_password ):
       global eto
       global prep 
       et0 = [] 
       eto.append(0)
       eto.append(.5)
       prep = 0
       print("process cimis data")
       print os.getcwd()
       try:
          os.system("rm email_data/*")
       except:
          pass
       print "fetching email"
       x = MailBox(imap_username, imap_password)
       with  x as mbox:
           print("count",mbox.get_count())
           if mbox.get_count() > 0 :
              mbox.process_msgs()
              
           else:
              print "no messages" 
       
       print "messages fetch", os.getcwd()
      
       x.close
       print os.getcwd()
       os.system("rm email_data/*")
       return eto
 

def delete_cimis_email( imap_username, imap_password ):
       os.system("rm email_data/*")
       with MailBox(imap_username, imap_password) as mbox:
           print("count",mbox.get_count())
           if mbox.get_count() > 0 :
              mbox.delete_all()
           else:
              print "no messages" 
     
       os.system("rm email_data/*")
       os.system("ls email_data/*")
     

if __name__ == '__main__':
    # example:
#    while True:
#       imap_username = 'onyx.m2m.server@gmail.com'
#       imap_password = '#warton#'
       imap_username = 'lacima.ranch@gmail.com'
       imap_password = 'Gr1234gfd'
       print process_cimis_data(imap_username, imap_password)
