# NotesToCommands
NotesToCommands is a fully customizable notes / command template program, allowing users to instantly execute terminal commands with dynamic arguments grouped into sections in their notes/files. It was originally created for pentesting uses, to avoid the needed remembrance and retyping of sets of commands for various attacks.

## Identifyers and placeholders

Users can denominate section and command identifyers within userData.py. An example note file and data file is provided. Run this program as is to see it work.

To denominate placeholder argumeents in a command, use [brackets].

<pre><code>// ifconfig [adapter]
</pre></code>


By default, '//' will register the command in the options list (! only when it is within a section) and [adapter] will be an argument which must be provided at the prompt before execution. Arguments can be provided spaced apart immeditely after your selection, or they can be seperated with ' // ' if there are multiple word per argument. They will be assigned to the users denoted placeholders as appropriate. If none are specified yet placeholders exist within the selected command, the program will prompt the user for them one by one.

<pre><code>///// Basic Commands
// echo [placeholder1] [placeholder2]
</pre></code>

The program will display this within the menu as such:
<pre><code>[0] Basic Commands
   [0] echo [placeholder1] [placeholder2]</pre></code>

Then at the prompt, a user can enter 
<pre><code>0,0 hello world</pre></code><i>or</i><pre><code>0,0 hello world // this is a long string</pre></code>

If only a section selection is made, the program will prompt for the command selection as well. Users are also able to enter any native terminal command into the prompt - it will be executed as long as the program sees your input cannot convert to an integer, thus must not be a single section selection.

<i>I RECOMMEND REVIEWING THE CODE AS IT IS < 200 LINES, THEN THE EXAMPLE.TXT FILE TO SEE HOW USERS CAN IMPLEMENT THEIR SPECIFIED COMMAND AND SECTION IDENTIFYERS IN THEIR NOTES / FILES</i>
