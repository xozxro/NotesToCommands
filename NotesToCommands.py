####################################################
###
### Written by zxro 2021
### twitter.com/xozxro
###
####################################################
###
### NotesToCmd allows users to take notes on various terminal commands and then execute templates of with ease, right from
### their notes. denominate sections and commands within them inside userData.py.
### !! an example note file and data file has been provided. run this program and open example.txt to see it work.
###
### to denominate placeholder inputs in a command, users should use [brackets]
###
#### ie // ifconfig [adapter]
###
### '//' will register the command in the options list (! only when it is within a section) and [adapter] will be a argument
### which must be provided before execution. arguments can be provided spaced apart immeditely after your selection,
### or they can be seperated with ' // ' if there are multiple word per argument. they will be assigned to the denoted
### placeholders as appropriate.
###
#### i.e // echo [placeholder1] [placeholder2]
#### assuming echo is command 0 of section 0, user can enter '0,0 hello world' or 0,0 hello world // this is a long string
###
### if no arguments are given, the program will prompt for them placeholder by placeholder. if only a section is
### specified, the program will prompt for that selection as well.
### users are also able to enter any command into the prompt as well - it will be executed as long as the program
### sees your input cannot convert to an interger, thus must not be a single section selection.
###
### ! I RECOMMEND REVIEWING THIS PROGRAM AS IT IS SHORT AND YOU WILL UNDERSTAND THE LOGIC IT USES
###
####################################################

import os
import re
from userData import *
import subprocess

if sectionDelim[-1] != ' ': sectionDelim += ' '
if commandDelim[-1] != ' ': commandDelim += ' '

if __name__ == '__main__':

    catching = True
    while catching:
        # first open the note file, read each line into an array
        if notesPath == '':
            # defaults to notes.txt within working directory
            notesPath == 'notes.txt'

        with open(notesPath) as noteFile:
            rawText = noteFile.readlines()
            noteFile.close()

        # strip newlines and trailing spaces from each line
        noteLines = [x.strip() for x in rawText]

        # find indexes for new sections
        sectionIndexes = []
        for line in noteLines:
            if sectionDelim in line:
                sectionIndexes.append(noteLines.index(line))

        # divide commands in sections into arrays. place into dictionary so they can be
        # retrieved with ease using a key for the section and index for the command
        sections = {}
        for x in range(0,len(sectionIndexes)):
            if sectionIndexes[x] != sectionIndexes[-1]:
                # can do this in a large list compression
                sections[noteLines[sectionIndexes[x]].replace(sectionDelim, '').strip()] = [x.replace(commandDelim, '').strip() for x in noteLines[sectionIndexes[x]:sectionIndexes[x+1]] if commandDelim in x.strip() and sectionDelim not in x.strip()]
            else:
                sections[noteLines[sectionIndexes[x]].replace(sectionDelim, '').strip()] = [x.replace(commandDelim, '').strip() for x in noteLines[sectionIndexes[x]:] if commandDelim in x.strip() and sectionDelim not in x.strip()]

        # main user menu
        sectionNum = 0
        sectionIndexes = {}
        inputArgs = []

        print('-----------------------------------')
        for section,commands in sections.items():

            cmdNum = 0

            print('[' + str(sectionNum) + '] --> ' + section.upper())

            # set index to call section by
            sectionIndexes[str(sectionNum)] = section.strip()

            # increase section index
            sectionNum += 1

            # iterate through commands in section
            for command in commands:
                print('   [' + str(cmdNum) + '] ' + command)
                cmdNum += 1

            print('[x] View extras')

        print('-----------------------------------')

        # main run loop
        Running = True
        while Running:

            userInput = input('>>')

            # extras options
            if userInput.strip() == 'x':
                print('[a] Open notes file [' + notesPath + ']')
                print('[b] View notes file in terminal')
                print('[c] Refresh from notes file [' + notesPath + ']')
                print('[d] Change notes file and refresh')
                print('[e] Change delims and refresh')
                extraInput = input('> ')
                if extraInput.strip() == 'a': process = subprocess.Popen(['gedit',notesPath], stdout=subprocess.PIPE)
                if extraInput.strip() == 'b':
                    for line in noteLines: print(line.strip())
                if extraInput.strip() == 'c': Running = False
                if extraInput.strip() == 'd':
                    notesPath = input('Notes path > ')
                    Running = False
                if extraInput.strip() == 'e':
                    sectionDelim = input('Section Delim > ')
                    commandDelim = input('Command Delim > ')
                    Running = False
                continue

            # deal with user input - did they pass arguments in first input?
            # does the program need to retrieve arguments for placeholders if not?
            # did they pass single - word arguments using spaces, or multi word arguments
            # using //? set variables appropriately
            if ' // ' in userInput and ',' in userInput:
                inputArgs = [x.strip() for x in userInput.split(' // ')]
                indexes = inputArgs[0].split(' ')[0].split(',')
                remove = inputArgs[0].split(' ')[0]
                inputArgs[0] = inputArgs[0].replace(remove,'').strip()
                print(inputArgs)
                sectionReqInd = indexes[0]
                commandReqInd = indexes[1]

            elif ' ' in userInput.strip() and ',' in userInput:
                inputArgs = userInput.split(' ')
                indexes = inputArgs[0].split(',')
                inputArgs = inputArgs[1:]
                print(inputArgs)
                sectionReqInd = indexes[0]
                commandReqInd = indexes[1]

            elif ',' in userInput:
                indexes = userInput.strip().split(',')
                sectionReqInd = indexes[0]
                commandReqInd = indexes[1]

            else:
                try:
                    int(userInput)
                    sectionReqInd = userInput
                    commandReqInd = input('CMD? > ')
                except:
                    try:
                        process = subprocess.Popen(userInput.split(), stdout=subprocess.PIPE)
                        output, error = process.communicate()
                    except:
                        print('Invalid command or file.')
                    continue

            # retreive selected command using the section saved under the first index, then
            # the command within the array assigned to that section via the second index
            selectedCommand = sections[sectionIndexes[sectionReqInd]][int(commandReqInd)]

            # check for placeholders
            if '[' in selectedCommand:

                # find them using regedit
                res = re.findall(r'\[.*?\]', selectedCommand)

                # check if user provided placeholder aguments already
                if inputArgs != [] and len(inputArgs) == len(res):

                    # replace within command accordingly
                    argNum = 0
                    for placeholder in res:
                        selectedCommand = selectedCommand.replace(placeholder,inputArgs[argNum])
                        argNum += 1

                else:

                    if inputArgs != []: print('Argument count != placeholder count')

                    # query user for placeholder arguments
                    for placeholder in res:
                        newPlaceholder = input(placeholder[1:-1] + ' = ')

                        # replace within command accordingly
                        selectedCommand = selectedCommand.replace(placeholder,newPlaceholder)

            finalCmd = selectedCommand

            # execute command
            process = subprocess.Popen(finalCmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            # return to the top of the loop to repeat
