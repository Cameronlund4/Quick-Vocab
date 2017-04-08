from enum import Enum


class Type(Enum):
    term = 1
    syn = 2
    ant = 3
    syn_ant = 4


class Indent:
    name = None  # Store the name of this
    indentNum = None  # Store the indent num of his

    def __init__(self, indentNum):
        self.indentNum = indentNum
        name = "indent"+str(indentNum)

    def printme(self):
        print(self.type)
