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
        if ("define" in indentData):
            self.tags[Tag.define] = bool(indentData["define"])
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

    def getQuizletPart(self, pointer, lastTerms):
        prefix = None
        suffix = None
        # Figure out the prefix and suffix
        if ("_" in pointer):
            prefix = pointer.split("_")[0].strip()
            suffix = pointer.split("_")[1].strip()
        else:
            prefix = pointer
        # If we're talking about this term
        if (prefix == "this"):
            if (suffix != None):  # We want our def
                return self.getDef()
            else:  # We want our term
                return self.term
        if (prefix.startswith("indent")):
            indentNum = int((prefix.strip())[6:])
            term = lastTerms[indentNum]
            if (suffix != None):  # We want terms def
                return term.getDef()
            else:  # We want terms... term
                return term.term

    def createQuizlets(self, lastTerms, quizletData):
        print("----> Quizlets:")
        for quizlet in self.quizlets:
            setData = self.quizlets[quizlet]
            only = setData.get("only")
            # If quizlet set requires only syn and this isn't one
            if ((only == "syn") & (not self.tags.get(Tag.synonym))):
                print("\tSkipping " + quizlet + ", this isn't a syn")
                continue  # Then continue
            # If quizlet set requires only ant and this isn't one
            if ((only == "ant") & (not self.tags.get(Tag.antonym))):
                print("\tSkipping " + quizlet + ", this isn't an ant")
                continue  # Then continue
            # Now that we know we should make a quizlet, do it
            # Grab the term and definition
            term = self.getQuizletPart(setData.get(
                "uses").split("|")[0].strip(), lastTerms)
            defin = self.getQuizletPart(setData.get(
                "uses").split("|")[1].strip(), lastTerms)
            quizletData.get(quizlet)[term] = defin
            print("\tCreated term for " + quizlet + ":")
            print("\t\t"+term+": "+defin)
