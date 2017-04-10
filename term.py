from enum import Enum


class Tag(Enum):
    synonym = 1
    antonym = 2
    ant = 3
    syn_ant = 4


class Term:
    indentName = None  # Store the name of this
    indentNum = None  # Store the indent num of his
    term = None # Store the term this object represents
    definition = None # Store the deinition for this term

    def __init__(self, indentNum, term, indentData):
        self.indentNum = indentNum
        indentName = "indent"+str(indentNum)
        self.term = term
        print("-")
        print(indentData)
        print("-")

    def getTerm(self):
        return self.term

    def getDef(self):
        return self.definition

    def hasDef(self):
        return self.defintion != None

    def define(self):
        # TODO define the term
        return
