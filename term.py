from enum import Enum


class Tag(Enum):
    synonym = 1
    antonym = 2
    syn_ant = 3
    define = 4


class Term:

    def __init__(self, indentNum, term, indentData, tags):
        self.definition = None
        self.tags = {Tag.synonym: False, Tag.antonym: False, Tag.define: True}
        self.indentNum = indentNum
        self.indentName = "indent" + str(indentNum)
        self.quizlets = indentData.get("quizlets")
        self.term = term
        self.tags.update(tags)
        print(str(self.tags))
        if (self.tags.get(Tag.define)):
            self.define()

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

    def createQuizlets(self, lastTerms, quizletData):
        print("Lolno")
        for quizlet in self.quizlets:
            setData = self.quizlets[quizlet]
            only = setData.get("only")
            # If quizlet set requires only syn and this isn't one
            if ((only == "syn") & (not self.tags.get(Tag.synonym))):
                print("Skipping " + quizlet + ", this isn't a syn")
                return
            # If quizlet set requires only ant and this isn't one
            if ((only == "ant") & (not self.tags.get(Tag.antonym))):
                print("Skipping " + quizlet + ", this isn't an ant")
                return  # Then return

            print(str(setData))
