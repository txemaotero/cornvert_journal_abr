#!/usr/bin/python
# -*- coding: utf-8 -*-


import unittest
from abbreviation import TitleAbbreviation


class TitleAbbreviationTest(unittest.TestCase):
    def setUp(self):
        self._TitAbb = TitleAbbreviation('data/journal_names_abr.dat')

    def test_convert2abbreviation(self):
        k = "Journal Of Chemical Physics"
        v = "J. Chem. Phys."
        self.assertEqual(self._TitAbb.convert2abbreviation(k), v)
        self.assertEqual(self._TitAbb.convert2title(v), k)
        k = "ChemPhysChem"
        v = "ChemPhysChem"
        self.assertEqual(self._TitAbb.convert2abbreviation(k), v)
        self.assertEqual(self._TitAbb.convert2title(v), k)


if __name__=="__main__":
    unittest.main()
