from enum import Enum
import math
import yaml
from term import Term

headerEndChar = '<'
spaceToTab = 2
headerDone = False
yamlText = ""
doc = open('/home/camer/Desktop/quick_vocab/testdoc.txt', 'r')
indentData = dict()
lastIndent = []
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


def clearIndentsUnder(indents, indentNum):
    for num in range(indentNum + 1, len(indents)):
        indents[num] = None

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


lastIndentCount = 0
print("Parsing file--------------------------------------")
with doc as inputFile:
    for line in inputFile:  # Iterate each line in the file
        if (not headerDone):  # If we're still reading the header
            if (line.startswith(headerEndChar)):  # If reached header end
                headerDone = True  # Stop processing as if reading header
                lastIndent = processYAML(yamlText)  # Process out all the YAML
                # We're done processing YAML, tell user
                print("> Parsing Body------------------------------------")
            else:  # If we haven't reached header end
                yamlText += line  # Add the line to the YAML string
        else:  # No longer reading header, handle as a term
            # Replace any harmful characters
            safeLine = line.replace('\n', ' ').replace('\r', '')
            # Get how indented this line is
            indentCount = int(math.floor(getIndent(safeLine)))
            # Now that we know indent, get rid of trails
            safeLine = safeLine.strip()
            print("--> Term: \"" + safeLine + "\"")
            # Create indent obj
            indent = Term(indentCount, safeLine, indentData[indentCount])
            print("----> Indent: " + str(indentCount))
            superIndent = lastIndent[indentCount -
                                     1] if (indentCount > 0) else None
            if not (superIndent == None):
                print("----> Super term: "+superIndent.getTerm())
            # Save this indent so children can use it later
            lastIndent[indentCount] = indent
            print("---------")
            # Manage clearing no longer relevant last indents
            if (indentCount < lastIndentCount):  # If we have moved smaller
                clearIndentsUnder(lastIndent, indentCount)  # Clear bigger
            lastIndentCount = indentCount  # Save this indent as the last
doc.close()
