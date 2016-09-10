#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this is a shitty script that replicates (9) in NetWiz
# Why not just use the (9) script you ask?
# reasons:
# - (9) doesn't work on a Mac w/o a lot of stuff. No ethtool. No arping. Output
# for similarly named tools is different fixing this would require the user to
# download a lot of stuff from either Homebrew or run this in a VM I think a VM
# is too heavyweight to deal with in a customer environment. Also, when you use
# a VM you can't use the neat built-in network stuff that Mac OS X has in scutil
# and networksetup Which brings me to:
# - Simpler, easier just to re-write (9)
#
# The bad news is this thing needs to get refactored. Like, BADLY. This script
# leans heavily on sh.py, a really neat Python lib that lets you write utterly
# horrible BASH-ish code then glue it all together using what pretends to be
# python.
#

import sys
try:
    import sh
except:
    print("You need sh.py installed!s")
    print("You should have gotten a copy of sh.py with this script from https://github.com/emarkham/connectivitytest.git")
    print("Or you can manually install sh.py via 'sudo pip install sh'")
    print("Or download sh.py from https://raw.githubusercontent.com/amoffat/sh/master/sh.py")
    sys.exit(1)

# neat trick, 'scutil --nwi' shows the active network interfaces that can connect to the internet
print("Checking IP addr assignment...")
iftable = {}
# interfaces = sh.grep(sh.scutil("--nwi"), "Network interfaces:")
try:
    interfaces = sh.awk(sh.grep(sh.scutil("--nwi"), "^Network interfaces:"), "-F", "Network interfaces: ", "{print $2}").split()
except:
    print("No IPv4/v6 states found, no valid interfaces identified, exiting")
    sys.exit(1)

# interfaces = sh.awk(sh.grep(sh.grep(sh.netstat("-i"), "en"), "-v", "<Link#"), "{print $1}").split()
# itmp = sh.grep(sh.grep(sh.netstat("-i"), "en"), "-v", "<Link#").split()
for i in interfaces:
    for j in sh.ifconfig(i):
        if "status: active" in j:
            networkservice = sh.egrep(sh.grep(sh.networksetup("-listnetworkserviceorder"), "-B1", i), "(\d)").split()[1]
            addr = sh.grep(sh.grep(sh.netstat("-n", "-I", i), "en0"), "-v", "Link#").split()[3]
            router = sh.grep(sh.networksetup("-getinfo", networkservice), "Router").split()[1]
            dnsserver = sh.grep(sh.sed(sh.scutil("--dns"), "-n", "-e", "/DNS configuration (for scoped queries)/,/Reach/p"), "nameserver").split()[2]
            iftable.update({i: [networkservice, addr, router, dnsserver]})

for intf in iftable:
    print("{} {} active".format(intf, iftable[intf][1]))
    if 'Wi-Fi' in iftable[intf][0]:
        # warn if interface is Wi-Fi, needs to be wired for a real connectivity test
        print("")
        print("##########################################################################")
        print("Warning: {} is a Wi-Fi interface! Tests will not be accurate!".format(intf))
        print("You should run this script connected the network same as the SSS")
        print("##########################################################################")
        sh.sleep(5)


# TODO: warn on 10/100 link connectivity (SSS only support 1G/10G)

print("\nChecking Gateway assignment...")
gateway_a = sh.grep(sh.route("-n", "get", "8.8.8.8"), "gateway").split()[1]
for intf in iftable:
    if iftable[intf][2] == gateway_a and ("Reachable" in sh.scutil("-r", iftable[intf][2])):
        print("Gateway is {}".format(gateway_a))
    else:
        print("Gateway misconfiguration")
        print(iftable[intf][2], gateway_a)
        sys.exit(1)

# TODO: check for duplicate IP assignment
# don't know how to programmatically check for IP conflict, maybe scutil has some stuff?
print("Checking gateway reachability by pinging gateway...")
for inf in iftable:
    for line in sh.ping("-c", "4", iftable[inf][2], _iter=True):
        print(line.rstrip('\n'))

print("")
print("Checking DNS server(s) reachability by pinging DNS server by IP, then do a DIG and see if we get a response...")
for inf in iftable:
    if iftable[inf][3]:
        dnsserver = iftable[inf][3]
        print("Checking if {} is reachable...".format(dnsserver))
        print("Pinging DNS server...")
        for line in sh.ping("-c", "4", dnsserver, _iter=True):
            print(line.strip('\n'))
        print("DNS server is {}".format(sh.scutil("-r", dnsserver)))
        print("")
        print("Resolving skycontrol.skyportsystems.com by dig...")
        if "Reachable" in sh.scutil("-r", "skycontrol.skyportsystems.com"):
            print("skycontrol.skyportsystems.com resolves to:")
            print(sh.dig("+short", "+identify", "skycontrol.skyportsystems.com"))
        else:
            print("Can't reach {}".format(dnsserver))
            sys.exit(1)

# TODO: perform reverse DNS lookup on this host
# 
# Running reverse-lookup on 172.18.181.11 (skysecure-1)...OK


# TODO: option to skip traceroute step (can be slow)
print("")
print("Running traceroute to skycontrol.skyportsystems.com (max 16 hops)")
for line in sh.traceroute("-m", 16, "-w", 1, "-n", "skycontrol.skyportsystems.com", _iter=True):
    print(line.rstrip('\n'))


print("")
print("Checking Proxy Configuration...")
proxymode = sh.networksetup("-getwebproxy",  networkservice)
if "Enabled: Yes" in proxymode:
    # TODO: check proxy connectivity
    # ProxyMode: http
    #                 proxy-wsa-esl.cisco.com.:8080
    # Ping proxy-wsa-esl.cisco.com....FAIL
    # Traceroute to proxy-wsa-esl.cisco.com....FAIL
    #                 Proxy proxy-wsa-esl.cisco.com.:8080 not reachable
    print(proxymode)
else:
    print("No proxy configured")


print("")
print("Checking http reachability  to http://skycontrol.skyportsystems.com using GET.")
print(sh.curl("-I", "http://skysecure.skyportsystems.com"))

print("")
print("Checking https reachability to https://skycontrol.skyportsystems.com using GET.")
print(sh.curl("-I", "https://skysecure.skyportsystems.com"))