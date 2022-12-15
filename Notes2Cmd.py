####################################################
###
### Written by zxro 2021
### github.com/xozxro
###
####################################################

import os
import re
from userData import *
import subprocess

if sectionID[-1] != ' ': sectionID += ' '
if commandID[-1] != ' ': commandID += ' '
useSudo = False

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
            if sectionID in line:
                sectionIndexes.append(noteLines.index(line))

        # divide commands in sections into arrays. place into dictionary so they can be
        # retrieved with ease using a key for the section and index for the command
        sections = {}
        for x in range(0,len(sectionIndexes)):
            if sectionIndexes[x] != sectionIndexes[-1]:
                # can do this in a large list compression
                sections[noteLines[sectionIndexes[x]].replace(sectionID, '').strip()] = [x.replace(commandID, '').strip() for x in noteLines[sectionIndexes[x]:sectionIndexes[x+1]] if commandID in x.strip() and sectionID not in x.strip()]
            else:
                sections[noteLines[sectionIndexes[x]].replace(sectionID, '').strip()] = [x.replace(commandID, '').strip() for x in noteLines[sectionIndexes[x]:] if commandID in x.strip() and sectionID not in x.strip()]

        # main user menu
        sectionNum = 0
        sectionIndexes = {}
        inputArgs = []

        print('-----------------------------------')
        for section,commands in sections.items():

            cmdNum = 0

            print('[' + str(sectionNum) + ']--> ' + section.upper())

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

            userInput = input(' > ')

            # extras options
            if userInput.strip() == 'x':
                print('[s] Execute all commands with sudo')
                print('[a] Open notes file [' + notesPath + ']')
                print('[b] View notes file in terminal')
                print('[c] Refresh from notes file [' + notesPath + ']')
                print('[d] Change notes file and refresh')
                print('[e] Change delims and refresh')
                extraInput = input('>> ')
                if extraInput.strip() == 's':
                    useSudo = True
                    continue
                if extraInput.strip() == 'a':
                    process = subprocess.Popen(['gedit',notesPath], stdout=subprocess.PIPE)
                    continue
                if extraInput.strip() == 'b':
                    for line in noteLines: print(line.strip())
                    continue
                if extraInput.strip() == 'c': Running = False
                if extraInput.strip() == 'd':
                    notesPath = input('Notes path > ')
                    Running = False
                if extraInput.strip() == 'e':
                    sectionDelim = input('Section Delim > ')
                    commandDelim = input('Command Delim > ')
                    Running = False
                else:
                    userInput = extraInput

            # deal with user input - did they pass arguments in first input?
            # does the program need to retrieve arguments for placeholders if not?
            # did they pass single - word arguments using spaces, or multi word arguments
            # using //? set variables appropriately
            if ' // ' in userInput and ',' in userInput:
                inputArgs = [x.strip() for x in userInput.split(' // ')]
                indexes = inputArgs[0].split(' ')[0].split(',')
                remove = inputArgs[0].split(' ')[0]
                inputArgs[0] = inputArgs[0].replace(remove,'').strip()
                sectionReqInd = indexes[0]
                commandReqInd = indexes[1]

            elif ' ' in userInput.strip() and ',' in userInput:
                inputArgs = userInput.split(' ')
                indexes = inputArgs[0].split(',')
                inputArgs = inputArgs[1:]
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
                placeholders = re.findall(r'\[.*?\]', selectedCommand)

                # check if user provided placeholder aguments already
                if inputArgs != [] and len(inputArgs) == len(placeholders):

                    # replace within command accordingly
                    argNum = 0
                    for placeholder in placeholders:

                        selectedCommand = selectedCommand.replace(placeholder,inputArgs[argNum])
                        argNum += 1

                else:

                    if inputArgs != []: print('Argument count != placeholder count')

                    # query user for placeholder arguments
                    for placeholder in placeholders:

                        newPlaceholder = input(placeholder[1:-1] + ' = ')
                        # replace within command accordingly
                        selectedCommand = selectedCommand.replace(placeholder,newPlaceholder)

            finalCmd = selectedCommand

            if useSudo: finalCmd = 'sudo ' + finalCmd

            # execute command
            process = subprocess.Popen(finalCmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            # return to the top of the loop to repeat
