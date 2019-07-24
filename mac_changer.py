#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="the_interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC Address")
    
    (options, arguments) = parser.parse_args()

    if not options.the_interface:
        parser.error("Please specify an interface, use --help for more info")
    elif not options.new_mac_address:
        parser.error("Please specify a new mac, use --help for more info")
    return options


def mac_changer(interface, new_mac):
    print("[+] Changing mac address of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(options):
    # Write Algorithm to make sure that the interface is changed
    ifconfig_result = subprocess.check_output(["ifconfig", options.the_interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0) # We want the 1st occurrence.
    else:
        print("Could not read MAC address.")

#(options, arguments) = get_arguments()
options = get_arguments()
#mac_changer(options.the_interface, options.new_mac_address)

# In the beginning, let's check mac address.
current_mac = get_current_mac(options)
print("Current MAC is " + str(current_mac))

mac_changer(options.the_interface, options.new_mac_address)

current_mac = get_current_mac(options)
if current_mac == options.new_mac_address:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("MAC address did not get changed")




#####################OUTPUT#####################
# root@kali:~/mac_changer# python mac_changer.py --i eth0 --m 00:11:22:33:44:22
# Current MAC is 00:11:22:33:44:33
# [+] Changing mac address of eth0 to 00:11:22:33:44:22
# [+] MAC address was successfully changed to 00:11:22:33:44:22
#
