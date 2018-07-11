#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import json
import string
import requests
import BeautifulSoup


class ExtracrAbbreviations(object):
    """
    This class manages the journal abbreviations mining.
    """
    BASE_URLS = ('https://images.webofknowledge.com/WOKRS520B4.1/help/WOS/{}_abrvjt.html'.format(i)
                 for i in ['0-9'] + list(string.ascii_uppercase))
    # Avoid, PRL B.
    EXPRESION = re.compile('[a-zA-Z]{2,}$')
    def __init__(self):
        self.session = requests.session()
        self.abbreviations = {}
        for url in self.BASE_URLS:
            print(f'Mining: "{url}"')
            self.mine_one_page(url)

    def mine_one_page(self, url):
        """
        Extract the abbreviations from one url.
        """
        content = BeautifulSoup.BeautifulSoup(self.session.get(url))
        titles = content.findAll('dt')
        abbrs = content.findAll('dd')
        assert len(titles) == len(abbrs)
        for title, abbr in zip(titles, abbrs):
            self._add_title_abbr(title.text, abbr.text)

    def _add_title_abbr(self, title, abbr):
        tit = title.title()
        abb = abbr.title()
        if title == abbr:
            self.abbreviations[tit] = abb
            return
        abb = abb.replace(' ', '. ')
        if self.EXPRESION.findall(abb):
            abb += '.'
        self.abbreviations[tit] = abb

    def save_abbr(self, fname='journal_names_abr.dat'):
        """
        Writes a .json with the mined abbreviations.
        """
        with open(fname, 'w') as _file:
            json.dump(self.abbreviations, _file, indent=4, sort_keys=True)
