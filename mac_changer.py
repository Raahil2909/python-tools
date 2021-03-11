import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address (eth0/wan0 etc ..)")
    parser.add_option("-m","--mac",dest="new_mac",help="new mac address that you want")
    (options,interface) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify the new MAC address, use --help for more info")
    return options


def change_mac(interface,new_mac):
    print("[+] Changing MAC address for "+interface+" to "+new_mac)

    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    if mac_address_result:
        return mac_address_result.group(0)
    else :
        print("[-] Could not get the MAC address.")


options = get_arguments()
curr_mac = get_mac_address(options.interface)
print("MAC : "+curr_mac)
change_mac(options.interface,options.new_mac)
curr_mac = get_mac_address(options.interface)
if(curr_mac==options.new_mac):
    print("[+] MAC address successfully changed to "+curr_mac)
else :
    print("[-] MAC address did not get changed ")

