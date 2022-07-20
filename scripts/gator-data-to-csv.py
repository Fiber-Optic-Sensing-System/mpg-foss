"""
Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
Collects data from the Gator hardware (or simulator) and saves it to a CSV file.
"""
import pandas as pd
from halo import Halo
from fosmodule import bcolors, bsymbols, GatorPacket, packetsim

#TODO: Edit GatorHW class to use the correct device ids.
#TODO: Check GatorData class to make sure it aligns with spec.
#TODO: Check that classes such as GatorHW are being initialized correctly.
#TODO: Implement timed collection not just one sample.
#TODO: Output collected data into CSV file using pandas.

#False inputs for testing                                                  type  version
#fakelis = bytearray((0x00, 0x00, 0x00, 0x2B))                                                                                                                                                                                   second packet of data begins on new line           
lis = bytearray((0x00,0x00,0x00,0x2B,0x00,0x4c,0x4b,0x40, 0x01, 0x00, 0x01, 0x00, 0x6f, 0x68, 0x6f, 0x79, 0x00, 0x00, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
0x00,0x00,0x00,0x2B,0x00,0x4c,0x4b,0x40, 0x01, 0x00, 0x01, 0x00, 0x6f, 0x68, 0x6f, 0x79, 0x00, 0x00, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
0x00,0x00,0x00,0x2B,0x00,0x4c,0x4b,0x40, 0x01, 0x00, 0x01, 0x00, 0x6f, 0x68, 0x6f, 0x79, 0x00, 0x00, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01))
somedata = bytearray(lis)


#Dictionaries for buffer data
payloadDict = {}
cog_data_dict = {}


#Use methods defined in fosmodule to extract data from raw bytes.
somepacket = GatorPacket.header()
somepacket.data = somedata
some_packet_payload_len = somepacket.get_payload_len()
print(some_packet_payload_len)
some_packet_timestamp = somepacket.get_timestamp()
print(some_packet_timestamp)
some_packet_num = somepacket.get_packet_num()
print(some_packet_num)
some_gator_type = somepacket.get_gator_type()
print(some_gator_type)
some_version = somepacket.get_version()
print(some_version)
some_characters = somepacket.get_characters()
print(some_characters)

print("-----------------------------------------------------")

datapacket = GatorPacket.data()
datapacket.data = somedata
cog_data = datapacket.get_cog_data()
i = 0
for sensor in cog_data:
    print("Cog data from sensor ", i, " ", sensor)
    i += 1

print("-----------------------------------------------------")
simpacket = packetsim()
some_bytes = simpacket.generate_packets(2)
#print("Raw packet:", some_bytes.hex())
print("Raw packet:", some_bytes)
print("-----------------------------------------------------")

"""
def handle_args():
    parser = argparse.ArgumentParser(description='Run foss.py help for more information. Run foss.py deps to install dependencies.')
    parser.add_argument('-t', type=int, required=True)
    parser.add_argument('-o', type=str, required=True)
    args = parser.parse_args()
    return args
"""

"""
spinner = Halo(spinner='dots')
errorStatus = False
collectDuration = 0
fileName = ""
outputPath = ""
"""

"""
def get_endpoint():
    global errorStatus
    try:
        GatorHW.dev = usb.core.find(idVendor=GatorHW.v_id, idProduct=GatorHW.p_id)
        GatorHW.ep = GatorHW.dev[0].interfaces()[0].endpoints()[0]
        GatorHW.i = GatorHW.dev[0].interfaces()[0].bInterfaceNumber
    except:
        errorStatus = 1
"""

"""
def configuratuion():
    global errorStatus
    try:
        GatorHW.dev.reset()
        if GatorHW.dev.is_kernel_driver_active(GatorHW.inum):
            GatorHW.dev.detach_kernel_driver(GatorHW.inum)
        GatorHW.dev.set_configuration()
        GatorHW.eaddr = GatorHW.ep.bEndpointAddress
    except:
        errorStatus = 1
"""

"""
def read_data(len):
    global errorStatus
    try:
        data = GatorHW.dev.read(GatorHW.eaddr,len)
        return data
    except:
        errorStatus = 1
"""

def error_check():
    global errorStatus
    global spinner
    if errorStatus:
        spinner.text_color = 'red'
        spinner.fail("mpg-foss: Unhandled exception!")
        exit()
    else:
        spinner.text_color = 'green'
        spinner.succeed("mpg-foss: success!")
    spinner.start()

"""
#Run
try:
    args = handle_args()
    set_params(args)
    spinner.start()
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Looking for gator...{bcolors.ENDC}")
    get_endpoint()
    error_check()
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Setting USB configuration...{bcolors.ENDC}")
    configuratuion()
    error_check()
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: collecting data...{bcolors.ENDC}")
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Time: {collectDuration} Filename: {fileName}{bcolors.ENDC}")
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: receiving...{bcolors.ENDC}")
    GatorData.header.data = read_data(GatorData.header_len)
    error_check()
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: receiving...{bcolors.ENDC}")
    GatorData.status.data = read_data(GatorData.status_len)
    error_check()
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: receiving...{bcolors.ENDC}")
    GatorData.data.data = read_data(GatorData.data_len)
    error_check()
    spinner.text_color = 'green'
    spinner.succeed("mpg-foss: Done with timed data collection.")
    print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: File located at {outputPath}{bcolors.ENDC}")
except(KeyboardInterrupt, SystemExit):
    spinner.text_color = 'red'
    spinner.fail("mpg-foss: Process aborted.")
"""