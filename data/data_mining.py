#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import json
import string
import requests
import BeautifulSoup


# Se leen los tipos y se almacenan en un diccionario con el indice de clave
pages = ['0-9'] + list(string.ascii_uppercase)
url_base = 'https://images.webofknowledge.com/WOKRS520B4.1/help/WOS/{}_abrvjt.html'

dic = {}
expresion = re.compile('[a-zA-Z]{2,}$')
for i in pages:
    print('Extracting {}'.format(i))
    url = url_base.format(i)
    session = requests.session()
    req = session.get(url)
    doc = BeautifulSoup.BeautifulSoup(req.content)
    titles = doc.findAll('dt')
    abbr = doc.findAll('dd')
    for t, a in zip(titles, abbr):
        tit = t.text.title()
        abb = a.text.title().replace(' ', '. ')
        if expresion.findall(abb):
            abb += '.'
        dic[tit] = abb

with open('journal_names_abr.dat', 'w') as f:
    json.dump(dic, f, indent=4, sort_keys=True)
