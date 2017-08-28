'''
    This is my own ANML library so I don't have to use Micron's broken SDK
'''
from enum import Enum


class AnmlDefs(Enum):
    ALL_INPUT = 1
    NO_START = 2


class Ste(object):

    # anmlId, character_class, defs, match=False, reportCode=None):
    def __init__(self, *args, **kwargs):

        self.neighbors_ = []

        self.character_class_ = args[0]
        self.defs_ = args[1]
        self.starting_ = False
        self.reportCode_ = None
        self.matching_ = False

        self.id_ = str(kwargs['anmlId'])

        if 'reportCode' in kwargs:
            self.reportCode_ = str(kwargs['reportCode'])

        if 'match' in kwargs:
            self.matching_ = kwargs['match']

        if self.defs_ == AnmlDefs.ALL_INPUT:
            self.starting_ = True
            self.start_type_ = 'all-input'

    def add_edge(self, ste2):
        self.neighbors_.append(ste2)

    def __str__(self):
        string = "<state-transition-element id=\"" + self.id_ + \
            "\" symbol-set=\"" + self.character_class_ + "\""
        if self.starting_:
            string += " start=\"" + self.start_type_ + "\">\n"
        else:
            string += ">\n"
        if self.reportCode_ is not None:
            string += "\t\t\t<report-on-match reportcode=\"" +\
                self.reportCode_ + "\"/>\n"
        for neighbor in self.neighbors_:
            string += "\t\t\t<activate-on-match element=\"" + \
                neighbor.id_ + "\"/>\n"
        string += "\t\t</state-transition-element>\n"
        return string


class Anml(object):

    def __init__(self, aId="an1"):
        self.stes_ = []
        self.id_ = aId

    def __str__(self):
        string = "<anml version=\"1.0\"  xmlns:xsi=\"\
            http://www.w3.org/2001/XMLSchema-instance\">\n"
        string += "\t<automata-network id=\"" + self.id_ + "\">\n"
        for ste in self.stes_:
            string += '\t\t' + str(ste)
        string += '\t</automata-network>\n'
        string += '</anml>\n'
        return string

    def AddSTE(self, *args, **kargs):

        ste = Ste(*args, **kargs)

        self.stes_.append(ste)
        return ste

    def AddAnmlEdge(self, ste1, ste2, stuff):

        ste1.add_edge(ste2)

    # Write the resulting Anml to a file
    def ExportAnml(self, filename):

        with open(filename, 'w') as f:
            f.write(str(self))
        return 0


if __name__ == "__main__":

    anml = Anml()

    stes = []

    report_symbol = r"\x%02X" % 255

    for i in range(10):
        if i == 0:
            start_ste = anml.AddSTE(report_symbol, AnmlDefs.ALL_INPUT,
                                    anmlId=i, match=False)
            stes.append(start_ste)
        else:
            character_class = r"\x%02X" % i
            ste = anml.AddSTE(character_class, AnmlDefs.NO_START,
                              anmlId=i, match=False)
            anml.AddAnmlEdge(stes[-1], ste, 0)
            stes.append(ste)

    ste = anml.AddSTE(report_symbol, AnmlDefs.NO_START,
                      anmlId=10, reportCode=10)
    anml.AddAnmlEdge(stes[-1], ste, 0)
    anml.ExportAnml("test_anml.anml")
