# NotesToCommands
NotesToCommands is a fully customizable notes experience, allowing users to instantly execute terminal commands with dynamic arguments grouped into sections in their notes. It was originally created for pentesting uses, to avoid the needed remembrance and retyping of sets of commands for various attacks.

NotesToCmd allows users to take notes on various terminal commands and then execute templates of with ease, right fromvtheir notes. user can denominate section and command identifyers within inside userData.py.

An example note file and data file is provided. Run this program as is to see it work.

To denominate placeholder inputs in a command, users should use [brackets].

 ie // ifconfig [adapter]

 By default, '//' will register the command in the options list (! only when it is within a section) and [adapter] will be a argument which must be provided before execution. Arguments can be provided spaced apart immeditely after your selection,vor they can be seperated with ' // ' if there are multiple word per argument. They will be assigned to the users denoted placeholders as appropriate.

 i.e // echo [placeholder1] [placeholder2]
 Assuming echo is command 0 of section 0, user can enter '0,0 hello world' or 0,0 hello world // this is a long string

If no arguments are given, the program will prompt for them placeholder by placeholder. If only a section selection is made, the program will prompt for the command selection as well.
 
Users are also able to enter any native terminal command into the prompt as well - it will be executed as long as the program sees your input cannot convert to an integer, thus must not be a single section selection.

! I RECOMMEND REVIEWING THE CODE AS IT IS ONLY ~200 LINES, THEN THE EXAMPLE FILE TO SEE HOW USERS CAN IMPLEMENT THEIR SPECIFIED COMMAND IDENTIFYERS IN THEIR NOTES.


