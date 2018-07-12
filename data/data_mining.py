#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import string
import requests

from titlecase import titlecase

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class ExtracrAbbreviations(object):
    """
    This class manages the journal abbreviations mining.
    """

    BASE_URLS = ['https://images.webofknowledge.com/WOKRS520B4.1/help/WOS/{}_abrvjt.html'.format(i)
                 for i in ['0-9'] + list(string.ascii_uppercase)]

    def __init__(self):
        self.session = requests.session()
        self.abbreviations = {}
        for i, url in enumerate(self.BASE_URLS):
            print(f'Mining: {i+1}/{len(self.BASE_URLS)}')
            self.mine_one_page(url)

    def mine_one_page(self, url):
        """
        Extract the abbreviations from one url.
        """
        content = BeautifulSoup(self.session.get(url).content, 'html5lib')
        titles = content.findAll('dt')
        abbrs = content.findAll('dd')
        assert len(titles) == len(abbrs)
        for title, abbr in zip(titles, abbrs):
            self._add_title_abbr(title.text, abbr.text)

    def _add_title_abbr(self, title, abbr):
        tit = titlecase(title.strip())
        abb = titlecase(abbr.strip())
        if title == abbr:
            self.abbreviations[tit] = abb
            return
        abb = add_dots_to_abb(tit, abb)
        self.abbreviations[tit] = abb

    def save_abbr(self, fname='journal_names_abr.dat'):
        """
        Writes a .json with the mined abbreviations.
        """
        with open(fname, 'w') as _file:
            json.dump(self.abbreviations, _file, indent=4, sort_keys=True)


def add_dots_to_abb(tit, abb):
    """
    Adds the necessary dots to the end of abb words.
    """
    # separate in words
    tit_s = tit.split(' ')
    abb_s = abb.split(' ')
    # If the word is in both sets, no need to add dot.
    coincidences = set(tit_s).intersection(abb_s)
    new_abb = []
    for abbr in abb_s:
        if (abbr in coincidences) or (not abbr) or (len(abbr) > 6):
            new_abb.append(abbr)
        else:
            new_abb.append(abbr + '.')
    return ' '.join(new_abb)


if __name__ == '__main__':
    extr = ExtracrAbbreviations()
    extr.save_abbr('test.dat')
