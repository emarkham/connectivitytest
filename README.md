# connectivitytest

This is a shitty script that replicates (9) in NetWiz. Sometimes it's easier to troubleshoot what's going on from your own laptop than to try from the USB console.

 "Why not just run the (9) script from your laptop," you ask?

 Reasons:

 - (9) doesn't work on a Mac w/o a lot of stuff

 No ethtool. No arping. Output for similarly named tools is different between the two platforms.
 Fixing this would require the user to download a lot of stuff from Homebrew or run in a VM.

 I think a VM is too heavyweight for running 1 simple script.

 Also, when you use a VM you can't use the neat built-in network stuff that Mac OS X has in 'scutil' and 'networksetup'.

 Which brings me to:

 - Simpler, easier

 The bad news is this code needs to get refactored. Like, BADLY.

 This script leans heavily on sh.py, a really neat Python lib that lets you write utterly horrible BASH-ish code
 then glue it all together using what pretends to be python.

# How to use

open Terminal, then do:

    git clone https://github.com/emarkham/connectivitytest.git
    cd connectivitytest
    ./connectivitytest.py

You should see some output. Hopefully that output will tell you why the SkySecure Server isn't reaching SkySecure Center.

# Tests the script runs:

- interface check
- pings the gateway
- DNS reachability check
- DNS resolution check
- route to SkySecure Center check
- proxy config check
- HTTP GET skycontrol.skyportsystems.com

# TODO:

- warn if interface is Wi-Fi
- 10/100 ethernet connecivity warning
- duplicate IP test
- reverse lookups for test laptop and against SSC
- option to skip traceroute
- proxy connectivity tests