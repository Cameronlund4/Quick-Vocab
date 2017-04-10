# Quick Vocab

Quick Vocab, or QuickVoc, is a program designed to do the busywork of vocabulary for you leaving more time to do what really matters: actually learning the material. Quick Vocab aims to supply a medium to quickly define your vocab and related items, make use of these definitons, and get right into studying. Quick Vocab takes in a text file which specifies what you want to do with your terms, followed by a list of your terms. It then processes these terms and will manipulate them to your heart's desire, doing things like creating quizlets and generating a study sheet.


#### Note: Still very much WIP. More information coming soon. 

-------------------------------------------------------------

### How it works:

QuickVoc will take a text file in that is seperated into two parts: the [header](https://github.com/Cameronlund4/Quick-Vocab/blob/master/README.md#yaml-header) and the [body](https://github.com/Cameronlund4/Quick-Vocab/blob/master/README.md#term-body). These are seperated by a `<` so the program knows where header stops and the body starts. The header tells the program what it needs to be doing and the body is where you write out the terms you want the program to handle. The format of the document is made to be extremely easy to type out, saving you as much time as possible. Here is how the program structure looks:

```
#
# This is where the YAML header goes
#

# This carrot tells the program that the header is done
# and that the following text is a part of the body
<

#
# This is where the raw text body goes
#
```

-------------------------------------------------------------

### YAML header:

QuickVoc uses a block of YAML at the beginning of the text file which tells it what it needs to be doing. This contains arguments like how to show the difference between synonyms and antonyms as well as defining what each different indent means.

```yaml
indent0: # Defining how to handle terms with no indent
  define: true # Telling QuickVoc that this term should be defined
  quizlets: # Telling QuickVoc to generate quizlets with this term
    Base Definitions: # Telling QuickVoc to create a set named 'Base Definitions'
      use: indent0|indent0_def # Tells QuickVoc to use the word as the term and the def as the def

indent1: # Defining how to handle terms with 1 tab or 2 spaces infront
  define: true # Telling QuickVoc that this term should be defined
  type: syn|ant # Tells QuickVoc that these terms are synonyms/antonyms of the above indent0 term
  quizlets: # Telling QuickVoc to generate quizlets with this term
    Synonyms: # Telling QuickVoc to create a set named 'Synonyms'
      use: indent1|indent0 # Tells QuickVoc to use indent1 as the term and above indent0 as the def
      only: syn # Tells QuickVoc to only use this quizlet format for words that are syn of indent0
    Antonyms: # Telling QuickVoc to create a set named 'Antonyms'
      use: indent1|indent0 # Tells QuickVoc to use indent1 as the term and above indent0 as the def
      only: syn # Tells QuickVoc to only use this quizlet format for words that are ant of indent0
    Base Definitions: # Yep, two indents can add terms to the same quizlet! (see indent0)
      use: indent1|indent1_def # Tells QuickVoc to use the word as the term and the def as the def
      
syncolor: green # Tells QuickVoc that synonyms should be colored green when displayed
antcolor: red # Tells QuickVoc that antonyms should be colored red when displayed
```

-------------------------------------------------------------

### Term body:

The body is formatted based on the indents you define in the YAML header. Two spaces or a tab both count as a single indent. When a indent references another indent (For example, if `indent1` is using `indent0` in a quizlet), it will reference the most recent use of that indent above. For that reason, an `indent1` should always be below an `indent0` at some point. Here is an example:

```yaml
Potato # This is an `indent0`
  Spud # This is an `indent1`, synynom to `indent0`
  Fries # This is an `indent1`, synynom to `indent0`
  Tomato # This is an `indent1`, antonym to `indent0`
    Something else # This is an `indent2`
```
(Note, `# Comments` don't currently work in the term body)

-------------------------------------------------------------

### How to Install:

Idk yet, give me some time :)

-------------------------------------------------------------

### Disclaimer:
This tool is created with the intent of making studying vocabulary easier, **_NOT_** to cheat on homework or any sort of assignment. You are responsible for how you use this tool and any trouble you get into by using it. Please read [our license](LICENSE.txt) before using this program.
