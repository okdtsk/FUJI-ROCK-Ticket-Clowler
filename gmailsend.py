#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

class sendGmail:
  def __init__(self, encoding, subject, body, from_addr, to_addr, login_addr, passwd):
	self.date = formatdate()
	self.encoding = encoding
	self.subject = subject
	self.body = body.encode('utf-8')
	self.from_addr = from_addr
	self.to_addr = to_addr
	self.login_addr = login_addr
	self.passwd = passwd

  def sendMail(self):
    msg = MIMEText(self.body, 'plain', self.encoding)
    msg['Subject'] = Header(self.subject, self.encoding)
    msg['From'] = self.from_addr
    msg['To'] = self.to_addr
    msg['Date'] = self.date

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(self.login_addr, self.passwd)
    s.sendmail(self.from_addr, self.to_addr, msg.as_string())
    s.close()
