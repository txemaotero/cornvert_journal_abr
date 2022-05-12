import json
import re
import sys
import os
from typing import Union

try:
    from titlecase import titlecase
except ImportError:
    raise ImportError("Please install titlecase (pip install titlecase)")


class TitleAbbreviation:
    """
    This class manage the conversion between titles and abbreviations.

    Parameters
    ----------
    title_data_files : str or list of str
        Path or paths to files with the data of journal titles and
        abbreviations in json format.
    """

    def __init__(self, title_data_files: Union[str, list]):
        if isinstance(title_data_files, str):
            title_data_files = [title_data_files]
        abbreviations = {}
        for title_data_file in title_data_files:
            with open(title_data_file) as _file:
                abbreviations.update(json.load(_file))
        self.abbreviations, self.inv_abbreviations = {}, {}
        for k, v in abbreviations.items():
            if not v or not k:
                continue
            self.abbreviations[k] = v
            self.inv_abbreviations[v] = k

    def convert_to_abbreviation(self, title: str) -> str:
        """
        Converts a title in anto abbreviation if its possible.
        """
        title = titlecase(title).strip()
        if title.startswith("The "):
            title = title[4:]
        if "\&" in title:
            title = title.replace("\&", "and")
        if "Applied Chem" in title:
            print(title in self.abbreviations)
        try:
            return self.abbreviations[title]
        except KeyError:
            raise KeyError("The input title is not in the data bank.")

    def convert_to_title(self, abbreviation: str) -> str:
        """
        Converts an abbreviation into a title if its possible.
        """
        abb = titlecase(abbreviation).strip()
        try:
            return self.inv_abbreviations[abb]
        except KeyError:
            raise KeyError("The input abbreviation is not in the data bank.")

    def convert_bib(self, fbib: str, fout: str = None):
        """
        Abbreviates all journal Titles of a .bib file.

        Parameters
        ----------
        fbib : str
            The path with the .bib file to convert.
        fout : str
            The path with the .bib file to write the results of conversion.
            If None: fout = fbib[:-4] + '_abbreviated.dat'
        """
        if fout is None:
            fout = fbib[:-4] + "_abbreviated.bib"
        changes: dict[str, set[str]] = {"Abbreviated": set(), "Not abbreviated": set()}
        _file = open(fbib)
        _gfile = open(fout, "w")
        for line in _file:
            if line.strip().lower().startswith("journal"):
                tit = re.findall("\{(.*?)\}", line)
                try:
                    title = tit[0]
                    abb = self.convert_to_abbreviation(title)
                    new_l = line.replace(title, abb)
                    changes["Abbreviated"].add(title)
                except IndexError:
                    raise IOError(
                        (
                            "The following journal line in the .bib"
                            "has a wrong format:\n{}"
                        ).format(line)
                    )
                except KeyError:
                    # Check if title is already an abbreviation
                    if tit[0] in self.inv_abbreviations:
                        new_l = line
                    elif tit[0] + '.' in self.inv_abbreviations:
                        new_l = line.replace(tit[0], tit[0] + '.')
                    else:
                        changes["Not abbreviated"].add(tit[0])
                        new_l = line

                _gfile.write(new_l)
            else:
                _gfile.write(line)
        _gfile.close()
        _file.close()
        print("The abbreviated titles are:\n")
        print("\t" + "\n\t".join(changes["Abbreviated"]) + "\n\n")
        print("The following titles were not found in the data bank:\n\t")
        print("\t" + "\n\t".join(changes["Not abbreviated"]))


def convert_bib(inp: str, out: str = None):
    """
    Modify this function to find the path to journal_names.dat
    """
    current = os.path.dirname(os.path.abspath(__file__))
    rel_paths = ("data/journal_names_abr.dat", "data/journal_names_abr_added.dat")
    data = [os.path.join(current, rel_p) for rel_p in rel_paths]
    titabb = TitleAbbreviation(data)
    titabb.convert_bib(inp, out)


if __name__ == "__main__":
    INP, OUT = sys.argv[1:3]
    convert_bib(INP, OUT)
