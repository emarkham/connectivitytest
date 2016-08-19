# connectivitytest

this is a shitty script that replicates (9) in NetWiz
 
 Why not just use the (9) script you ask?
 
 reasons:
 
 - (9) doesn't work on a Mac w/o a lot of stuff. No ethtool. No arping. Output for similarly named tools is different
 fixing this would require the user to download a lot of stuff from either Homebrew or run this in a VM
 
 I think a VM is too heavyweight to deal with.
 
 Also, when you use a VM you can't use the neat built-in network stuff that Mac OS X has in scutil and networksetup
 
 Which brings me to:
 
 - Simpler, easier

 The bad news is this thing needs to get refactored. Like, BADLY.
 
 This script leans heavily on sh.py, a really neat Python lib that lets you write utterly horrible BASH-ish code
 then glue it all together using what pretends to be python.

