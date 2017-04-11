# Dependents:
#  - Must be run with python3 for enums
#  - Needs python-docx to build the word files

from enum import Enum
import math
import yaml
from term import Term
from term import Tag
from docx import Document
from docx.shared import Inches

headerEndChar = '<'
spaceToTab = 2
headerDone = False
yamlText = ""
doc = open('/home/camer/Desktop/quick_vocab/testdoc.txt', 'r')
outputFile = open('/home/camer/Desktop/quick_vocab/testout.txt', 'w')
indentData = dict()
lastTerms = []
quizlets = dict()  # Create a dictionary to store quizlet terms

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


def getIndent(message):
    if (message.startswith(" ")):
        return getIndent(message[1:]) + (1 / spaceToTab);
    elif (message.startswith("\t")):
        return getIndent(message[1:]) + 1;
    else:
        return 0

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


def processYAML(yamlText):
    global quizlets
    global indentData
    indentLen = 0
    print("> Parsing YAML------------------------------------")
    yamlData = yaml.load(yamlText)  # Load YAML string to object
    for arg in yamlData:  # For each indent...
        argData = yamlData.get(arg)
        if (arg.startswith("indent")):
            print("--> Indent: " + arg)
            # Check if this is the biggest indent yet
            thisIndentLen = int(arg[6:])
            print("----> Depth: " + str(thisIndentLen))
            if (thisIndentLen + 1 > indentLen):
                indentLen = thisIndentLen + 1
            # Save the YAML to construct indents later
            indentData[thisIndentLen] = argData
            # Document any quizlets so we can store them later
            if ("quizlets" in argData):
                # Iterate each of the indents quizlets
                for quizlet in argData.get("quizlets"):
                    # If we don't already have a spot for this quizlet set
                    if not (quizlet in quizlets):
                        # Create a dictionary (quizterm:quizdef)
                        quizlets[quizlet] = dict()
        else:
            print("--> Argument: " + arg)
        print("----> " + str(argData))
    return [None] * indentLen  # Create a list to store indents and return


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


def processBody(line):
    global lastIndentNum, lastTerms, quizlets
    # Replace any harmful characters
    safeLine = line.replace('\n', ' ').replace('\r', '')
    # Get how indented this line is
    indentNum = int(math.floor(getIndent(safeLine)))
    # Now that we know indent, get rid of trails
    safeLine = safeLine.strip()
    print("--> Term: \"" + safeLine + "\"")
    # Check for any special case tags
    if safeLine.startswith("i:"):  # Ignored line
        return
    # Create term obj
    term = Term(indentNum, safeLine, indentData[indentNum], {})
    print("----> Indent: " + str(indentNum))
    superIndent = lastTerms[indentNum -
                            1] if (indentNum > 0) else None
    if not (superIndent == None):
        print("----> Super term: " + superIndent.getTerm())
    # Write the line
    outputFile.write(term.getLine())
    # Create any quizlets
    term.createQuizlets(lastTerms, quizlets)
    # Save this term so children can use it later
    lastTerms[indentNum] = term
    print("---------")
    # Manage clearing no longer relevant last terms
    if (indentNum < lastIndentNum):  # If we have moved smaller
        clearIndentsUnder(lastTerms, indentNum)  # Clear bigger
    lastIndentNum = indentNum  # Save this term as the last

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


def clearIndentsUnder(indents, indentNum):
    for num in range(indentNum + 1, len(indents)):
        indents[num] = None

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


lastIndentNum = 0
print("Parsing file--------------------------------------")
with doc as inputFile:
    # Iterate each line in the file and process it
    for line in inputFile:
        if (not headerDone):  # If we're still reading the header
            if (line.startswith(headerEndChar)):  # If reached header end
                headerDone = True  # Stop processing as if reading header
                lastTerms = processYAML(yamlText)  # Process out all the YAML
                # We're done processing YAML, tell user
                print("> Parsing Body------------------------------------")
            else:  # If we haven't reached header end
                yamlText += line  # Add the line to the YAML string
        else:  # No longer reading header, handle as a term
            processBody(line);
    # Now that terms are processed and defined, make quizlets
    # TODO Use the quizlets dict to generate quizlets
outputFile.close()
doc.close()
