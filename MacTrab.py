import random, string, optparse, subprocess, os, re


def getOptions():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC address. if not specified, random MAC will be generated")

    options = parser.parse_args()[0]
    return options


def changeMac(interface, newMac):
    fnull = open(os.devnull, 'w')
    subprocess.call(["ifconfig", interface, "down"], stdout=fnull, stderr=subprocess.STDOUT)
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac], stdout=fnull, stderr=subprocess.STDOUT)
    subprocess.call(["ifconfig", interface, "up"], stdout=fnull, stderr=subprocess.STDOUT)


def generateMac():
    first_part=""
    second_part=""

    for i in range(6):
        first_part += ''.join(random.choice("02468ace"))
        if (i % 2 != 0):
            first_part = first_part+":"

    for i in range(6):
        second_part += ''.join(random.choice("0123456789abcdef"))
        if (i % 2 != 0) and i < 4:
            second_part = second_part+":"

    return first_part + second_part


def checkOptions(interface, mac):
    if interface is not None:
        fnull = open(os.devnull, 'w')
        output = subprocess.call(["ifconfig", interface], stdout=fnull, stderr=subprocess.STDOUT)
        if output:
            print "ERROR: Could not find specified interface"
            return False
    else:
        print "ERROR: No interface specified"
        return False
    if mac is not None:
        check = re.search(r"^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w$", mac)
        if not check:
            print "ERROR: MAC format incorrect"
            return False
    return True



def checkChange(mac, interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    if not current_mac:
        print "ERROR: Could not find MAC address on specified interface"
        return False
    if current_mac.group(0) != mac:
        print "ERROR: Could not change MAC. Check your permissions"
        return False
    return True


options = getOptions()
interface = options.interface
if checkOptions(options.interface, options.newMac):
    if options.newMac is None:
        print "no MAC specified. Generating random MAC..."
        newMac = generateMac()
        print "new MAC generated! " + newMac
    else:
      newMac = options.newMac

    changeMac(interface, newMac)
    if checkChange(newMac, interface):
        print "MAC successfully changed to : " + newMac