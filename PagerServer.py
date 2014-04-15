#!/usr/bin/python3

# Server for printing mail to display

from smtpd import SMTPServer
from newScreen import lcd
import datetime

import threading

class pagerServer(SMTPServer):

  def __init__(self,localaddr,remoteaddr,createdInterface):
    super(pagerServer,self).__init__(localaddr,remoteaddr)
    self.iface = createdInterface

  def process_message(self, peer, mailfrom, rcpttos, data):
    output = open("Post",'a')
    dateSTR = ">Date; "+str(datetime.datetime.now())+"\n"
    output.write(dateSTR)
    fromSTR = ">Mail from: "+mailfrom+"\n"
    output.write(fromSTR)
    output.write("\n")
    output.write(data)
    output.write("\n")
    output.write("---\n\n")
    output.close()

    messageData = dateSTR+fromSTR+"\n\n"+data

    thread = threading.Thread(target = self.iface.newMail, args=(messageData,))
    thread.start()

