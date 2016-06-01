#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Asier Carreño
# Email: ascalotoru [at] gmail [dot] com
# Busca en la tienda de BQ y comprueba que haya stock del BQ Aquaris X5 Rosa

import urllib2
import smtplib
import time
from pushbullet import Pushbullet
from bs4 import BeautifulSoup

SMTP_Server = ""
SMTP_Port = ""
SMTP_User = ""
SMTP_Password = ""

PUSH_APIKEY = ""

fromaddr = ""
toaddrs = ""
subject = "Hay rosa en la tienda de BQ"
msg = "Hay rosa. Corre!!!!"

def mandar_email():
	try:
		servidor = smtplib.SMTP(SMTP_Server, SMTP_Port)
		servidor.starttls()
		servidor.login(SMTP_User, SMTP_Password)
		servidor.sendmail(fromaddr, toaddrs, msg)
	except as e:
		print time.strftime("%a %H:%M:%S") + " error en el envío de email", e
	else:
		servidor.quit()

def mandar_push():
	p = Pushbullet(PUSH_APIKEY)
	p.push_note("Hay rosa!", "Corre que hay rosa.")

print time.strftime("%a %H:%M:%S") + " hay_rosa: Me inicio"

openurl = urllib2.urlopen("https://store.bq.com/es/aquaris-x5")
soup = BeautifulSoup(openurl, "html.parser")
sp = soup.find_all("label", "inline_element")
for s in sp:
	nombre = s.contents[0].string.encode("utf-8")
	if nombre.lower().find("rosa") != -1:
		mandar_email()
		mandar_push()
