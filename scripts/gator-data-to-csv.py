"""
Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
Collects data from the Gator hardware (or simulator) and saves it to a CSV file.
"""
#import pandas as pd
from halo import Halo
from formatmodule import bcolors, bsymbols
from fosmodule import gatorpacket, packetsim

#Initialize
spinner = Halo(spinner='dots')
errorStatus = False
collectDuration = 0
fileName = ""
outputPath = ""
#Number of packets to simulate
num_packets = 25

def error_check():
    global errorStatus
    global spinner
    if errorStatus:
        spinner.text_color = 'red'
        spinner.fail("mpg-foss: Unhandled exception!")
        exit()
    else:
        spinner.text_color = 'green'
        spinner.succeed("mpg-foss: Success!")
    spinner.start()

try:
    #Instantiate a packet simulator.
    spinner.start()
    simpacket = packetsim()
    #Generate num packets.
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Generating {num_packets} packets...{bcolors.ENDC}")
    somedata = simpacket.generate_packets(num_packets)
    if(somedata == None):
        errorStatus = True
    error_check()
    #Use methods defined in fosmodule to extract data from raw bytes.
    somepacket = gatorpacket()
    somepacket.header.data = somedata
    #print(somepacket.data.hex()) #Debug
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Parsing packets...{bcolors.ENDC}")
    yoho = somepacket.header.get_characters()
    if(yoho == False):
        errorStatus = True
    error_check()
    ### Get data from packet ###
    some_packet_payload_len = somepacket.header.get_payload_len()
    some_packet_timestamp = somepacket.header.get_timestamp()
    some_packet_num = somepacket.header.get_packet_num()
    some_gator_type = somepacket.header.get_gator_type()
    some_version = somepacket.header.get_version()
    
    spinner.stop()
    ### Print data from packet ###
    print(f" Packet num: {some_packet_num} -> recorded at {some_packet_timestamp}μs collection time.")
    print(f" DEBUG: Payload len: {some_packet_payload_len} bytes | Gator type: {some_gator_type} | Gator version: {some_version}") #Debug

    #TODO: Get packet info from all packets in the buffer.

    #print("-----------------------------------------------------")
except(KeyboardInterrupt, SystemExit):
    spinner.text_color = 'red'
    spinner.fail("mpg-foss: Process aborted.")
