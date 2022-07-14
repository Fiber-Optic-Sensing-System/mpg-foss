"""
Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
Collects data from the Gator hardware (or simulator) and saves it to a CSV file.
"""
from abc import abstractclassmethod
from ast import Global
import usb.core
#import time
#import pandas
import argparse
from halo import Halo
from fosmodule import bcolors, bsymbols, GatorPacket

#TODO: Edit GatorHW class to use the correct device ids.
#TODO: Check GatorData class to make sure it aligns with spec.
#TODO: Check that classes such as GatorHW are being initialized correctly.
#TODO: Implement timed collection not just one sample.
#TODO: Output collected data into CSV file using pandas.

#False inputs for testing                                                  type  version
lis = bytearray((0x00,0x01,0x51,0x94,0x00,0x4c,0x4b,0x40, 0x01, 0x00, 0x01, 0x00, 0x6f, 0x68, 0x6f, 0x79, 0x00, 0x00, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01))
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


datapacket = GatorPacket.data()
datapacket.data = somedata
cog_data = datapacket.get_cog_data()
print(cog_data)



class Data:

    def __init__ (self, endpoint, buffer):
        self.endpoint = endpoint 
        self.buffer = buffer 
        buffer = []

    def read(endpoint, buffer, time): 
        buffer = payloadDict
        return 
        

    def sort(buffer):
        ret_val = 0
        i = 0 
        is_sync = False
        while (not is_sync and i < len(buffer)):
            if buffer[i] == 'y' and buffer[i+1] == 'o' and buffer[i+2] == 'h' and buffer[i+3] == 'o':
                is_sync = True
                ret_val = i - 15
            else: 
                i = i + 4
        payload_beginning = i + 1
        payload_end = somepacket.get_payload_len() + payload_beginning
        global payloadDict
        payloadDict.update({somepacket.get_packet_num(): somedata[payload_beginning:payload_end]})
        timestamp_beginning = ret_val + 4
        timestamp_end = somepacket.get_timestamp() + timestamp_beginning
        return ret_val, payload_beginning, payload_end, timestamp_beginning, timestamp_end

    def sortcog(cog_data_dict, payload_beginning, payload_end):
        cog_data_beginning = payload_beginning + 3
        cog_data_end = payload_beginning + 26
        cog_data_status = False
        if (cog_data_end == payload_end): 
            cog_data_status = True 
            if cog_data_status == 'True' :
                cog_data_dict.update({datapacket.get_cog_data(): somedata[cog_data_beginning:cog_data_end]})
        return cog_data_beginning, cog_data_end




    
    
    ex = sort(lis)
    print(ex)
    cogsorted = sortcog(cog_data_dict, ex[1], ex[2])
    print(cogsorted)

    
"""
def handle_args():
    parser = argparse.ArgumentParser(description='Run foss.py help for more information. Run foss.py deps to install dependencies.')
    parser.add_argument('-t', type=int, required=True)
    parser.add_argument('-o', type=str, required=True)
    args = parser.parse_args()
    return args

spinner = Halo(spinner='dots')
errorStatus = False
collectDuration = 0
fileName = ""
outputPath = ""

def set_params(args):
    global collectDuration
    global fileName
    global outputPath
    collectDuration = args.t
    fileName = args.o
    outputPath = "./data/" + fileName + ".csv"

class GatorHW:
    v_id = 0x045e
    p_id = 0x0040
    dev = usb.core.Device
    ep = usb.core.Endpoint
    inum = int
    eaddr = int

#TODO: Check the data structure.
#NOTE: I believe the output of the gator to be the following:
# - packet:[header (16 bytes), status (19 bits), sensor data (152 bits)] 299 bits, round to 38 bytes?
# - Use bytearray e.g.: somebytes = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]) bit bashing
class GatorData:
    header_len = 16
    status_len = 3
    data_len = 23 
    class header:
        data = [None] * 16
        payload_size = data[0:3]
        time_stamp = data[4:7]
        pkt_count = data[8:9]
        gator_type = data[10]
        gator_version = data[11]
        sync = data[12:15]
    class status:
        data = [None] * 19
        num_sens_found = data[1:4]
        sensor_ok = data[5:12]
        tec_temp_ok = data[13]
        sequence_num = data[14:18]
    class data:
        data = [None] * 19
        cog_data = data[0:17]
        sensor_error = data[18]

def get_endpoint():
    global errorStatus
    try:
        GatorHW.dev = usb.core.find(idVendor=GatorHW.v_id, idProduct=GatorHW.p_id)
        GatorHW.ep = GatorHW.dev[0].interfaces()[0].endpoints()[0]
        GatorHW.i = GatorHW.dev[0].interfaces()[0].bInterfaceNumber
    except:
        errorStatus = 1


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

def read_data(len):
    global errorStatus
    try:
        data = GatorHW.dev.read(GatorHW.eaddr,len)
        return data
    except:
        errorStatus = 1

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