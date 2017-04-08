from enum import Enum
import math
import yaml
import indent

headerEndChar = '<'
spaceToTab = 2
headerDone = False
yamlText = ""
doc = open('/home/camer/Desktop/quick_vocab/testdoc.txt', 'r')
lastIndent = []

def getIndent(message):
    if (message.startswith(" ")):
        return getIndent(message[1:]) + (1 / spaceToTab);
    elif (message.startswith("\t")):
        return getIndent(message[1:]) + 1;
    else:
        return 0

def processYAML(yamlText):
    indentLen = 0
    print("> Parsing YAML----------------")
    yamlData = yaml.load(yamlText) # Load YAML string to object
    for arg in yamlData: # For each indent...
        if (arg.startswith("indent")):
            print("--> Indent: " + arg)
            # Check if this is the biggest indent yet
            thisIndentLen = int(arg[6:])
            print("----> Depth: "+str(thisIndentLen))
            if (thisIndentLen > indentLen):
                indentLen = thisIndentLen
        else:
            print("--> Argument: "+arg)
        print("----> "+str(yamlData.get(arg)))
    return [None] * indentLen; # Create a list to store indents and return


print("Parsing file-----------------")
with doc as inputFile:
    for line in inputFile: # Iterate each line in the file
        if (not headerDone): # If we're still reading the header
            if (line.startswith(headerEndChar)): # If reached header end
                headerDone = True # Stop processing as if reading header
                lastIndent = processYAML(yamlText); # Process out all the YAML
                # We're done processing YAML, tell user
                print("> Parsing Body----------------")
            else: # If we haven't reached header end
                yamlText += line # Add the line to the YAML string
        else: # No longer reading header, handle as a term
            print("--> Term: " + line)
            indentCount = int(math.floor(getIndent(line)))
            print("----> Indent: " + str(indentCount))
doc.close()
