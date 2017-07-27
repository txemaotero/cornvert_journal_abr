#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import re
import sys




class TitleAbbreviation(object):
    """
    This class manage the conversion between titles and abbreviations.

    Attributes
    ----------
    title_data_files : string (file name) or list of strings
        The path with the data of journal titles and abbreviations. Or a list
        with multiple paths.
    abbreviations : dictionary {string: string}
        A dictionary with the journal titles as keys and its abbreviations as
        values.
    """
    def __init__(self, title_data_files):
        super(TitleAbbreviation, self).__init__()
        if isinstance(title_data_files, str):
            title_data_files = [title_data_files]
        self._title_data_files = title_data_files
        self._abbreviations = {}
        for title_data_file in title_data_files:
            with open(title_data_file) as f:
                self._abbreviations.update(json.load(f))
        self._inv_abbreviations = {v: k for k, v in self._abbreviations.items()}

    def convert2abbreviation(self, title):
        """
        Converts a title in an abbreviation if its possible.
        """
        title = title.title().strip()
        if title.startswith('The '):
            title = title[4:]
        if '\&' in title:
            title = title.replace('\&', u'&Amp;')
        try:
            return self._abbreviations[title]
        except KeyError:
            # Check if title is already an abbreviation
            chek1 = title in self._inv_abbreviations
            chek2 = title+'.' in self._inv_abbreviations
            if chek1:
                return title
            if chek2:
                return title+'.'
            raise(KeyError('The input title is not in the data bank.'))

    def convert2title(self, abbreviation):
        """
        Converts a title in an abbreviation if its possible.
        """
        abb = abbreviation.title().strip()
        try:
            return self._inv_abbreviations[abb]
        except KeyError:
            raise(KeyError('The input abbreviation is not in the data bank.'))

    def convert_bib(self, fbib, fout=None):
        """
        Abbreviates all journal Titles of a .bib file.

        Parameters
        ----------
        fbib : string - file name
            The path with the .bib file to convert.
        fout : string - file name (Optional)
            The path with the .bib file to write the results of conversion.
            If None: fout = fbib[:-4] + '_abbreviated.dat'
        """
        if fout is None:
            fout = fbib[:-4] + '_abbreviated.bib'
        changes = {'Abbreviated': set(),
                   'Not abbreviated': set()}
        f = open(fbib)
        g = open(fout, 'w')
        for l in f:
            if l.strip().startswith('journal'):
                tit = re.findall('\{(.*?)\}', l)
                try:
                    t = tit[0]
                    abb = self.convert2abbreviation(t)
                    new_l = l.replace(t, abb)
                    changes['Abbreviated'].add(t)
                except IndexError:
                    raise(IOError(('The following journal line in the .bib'
                                   'has a wrong format:\n{}').format(l)))
                except KeyError:
                    changes['Not abbreviated'].add(tit[0])
                    new_l = l
                g.write(new_l)
            else:
                g.write(l)
        g.close()
        f.close()
        print('The abbreviated titles are:\n')
        print('\t' + '\n\t'.join(changes['Abbreviated']) + '\n\n')
        print('The following titles were not found in the data bank:\n\t')
        print('\t' + '\n\t'.join(changes['Not abbreviated']))

    @property
    def title_data_file(self):
        return self._title_data_file

    @property
    def abbreviations(self):
        return self._abbreviations

    @property
    def inv_abbreviations(self):
        return self._inv_abbreviations


def convert_bib(inp, out=None):
    datas = ['/home/txema/github/cornvert_journal_abr/data/journal_names_abr.dat',
             '/home/txema/github/cornvert_journal_abr/data/journal_names_abr_added.dat']
    TitAbb = TitleAbbreviation(datas)
    TitAbb.convert_bib(inp, out)


if __name__=="__main__":
    inp, out = sys.argv[1:3]
    convert_bib(inp, out)
