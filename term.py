# Dependents:
#  - Must be run with python3 for enums
#  - Needs python-docx to build the word files

from enum import Enum
from docx import Document
from docx.shared import Inches

class Tag(Enum):
    synonym = 1
    antonym = 2
    ant = 3
    syn_ant = 4
    define = 5


class Term:
    indentName = None  # Store the name of this
    indentNum = None  # Store the indent num of his
    term = None  # Store the term this object represents
    definition = None  # Store the definition for this term
    tags = dict()


    def __init__(self, indentNum, term, indentData, tags):
        self.indentNum = indentNum
        self.indentName = "indent" + str(indentNum)
        self.term = term
        self.tags.update(tags)
        print(self.getLine()[:-1])

    def getTerm(self):
        return self.term

    def getDef(self):
        return self.definition

    def hasDef(self):
        return self.defintion != None

    def define(self):
        # TODO define the term
        return "This is a defintion for the term \"" + self.term + "\""

    def getLine(self):
        return ("\t" * self.indentNum) + self.term +"\n"
