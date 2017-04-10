from enum import Enum

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
    tags = {Tag.define: True}

    def __init__(self, indentNum, term, indentData, tags):
        self.indentNum = indentNum
        self.indentName = "indent" + str(indentNum)
        self.term = term
        self.tags.update(tags)
        if (self.tags.get(Tag.define)):
            self.define()
        print(self.getLine()[:-1])

    def getTerm(self):
        return self.term

    def getDef(self):
        return self.definition

    def hasDef(self):
        return self.definition != None

    def define(self):
        # TODO define the term
        self.definition = "This is a defintion for the term \"" + self.term + "\""

    def getLine(self):
        if (self.hasDef()):
            return ("\t" * self.indentNum) + self.term + ": " + self.getDef() + "\n"
        else:
            return ("\t" * self.indentNum) + self.term + "\n"
