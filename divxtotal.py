#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Asier Carreño

import urllib
import urlparse
from urllib2 import urlopen
import sys
import os
from bs4 import BeautifulSoup

ROOT = "http://www.divxtotal.com"
rtorrent_watch_folder = "/home/asier/rtorrent/watch"

html = urlopen(sys.argv[1]).read()
soup = BeautifulSoup(html, "html.parser")

# Seleccionamos todos los td con la clase 'capitulonombre'
tds = soup.find_all("td", class_="capitulonombre")
for td in tds:
    file = urllib.URLopener()
    url = ROOT + td.a['href']
    split = urlparse.urlsplit(url)
    filename = split.path.split("/")[-1]
    file.retrieve(url, os.path.join(rtorrent_watch_folder, filename))

