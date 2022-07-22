"""
Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
Collects data from the Gator hardware (or simulator) and saves it to a CSV file.
"""
#import pandas as pd
import functools
from lib2to3.pgen2.pgen import DFAState
from halo import Halo
from formatmodule import bcolors, bsymbols, pretty
from fosmodule import datahelper, gatorpacket, packetsim
import pandas as pd
import os

#Initialize
spinner = Halo(spinner='dots')
errorStatus = False
collectDuration = 0
fileName = ""
outputPath = ""
#Number of packets to simulate
num_packets = 75

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

def main():
    global errorStatus
    global spinner
    global collectDuration
    global num_packets
    data_frames = []
    outputPath = './data/out.csv'
    try:
        #Init console status indicator
        spinner.start()
        ### Instantiate classes ###
        datum = datahelper()
        simpacket = packetsim()
        #-------------------------#
        #Set print option
        selection_made = False
        printout = False
        second_selection_made = False 
        save_to_csv = False
        #Generate given num of packets.
        print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Generating {num_packets} packets...{bcolors.ENDC}")
        simdata = simpacket.generate_packets(num_packets)
        if(simdata == None):
            errorStatus = True
        error_check()
        datum.raw_data = simdata
        #----------------------------------------------------------------------------------------------#
        ### Next, sort datum for packets ###
        print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Parsing packets...{bcolors.ENDC}")
        packets = datum.parse()
        print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: {len(packets)} packets found...{bcolors.ENDC}", end="")
        #----------------------------------------------------------------------------------------------#
        ### Then get, values from each packet ###
        for key in packets:
            thispacket = gatorpacket()
            thispacket.raw_data = packets[key]
            #This tuple contains the inner class objects of the packet class.
            pkt_header, pkt_status, pkt_cog = thispacket.create_inner()
            #Pull out relevant values
            pkt_num = pkt_header.get_packet_num()
            pkt_timestamp = pkt_header.get_timestamp()
            pkt_payload_len = pkt_header.get_payload_len()
            gator_version = pkt_header.get_version()
            gator_type = pkt_header.get_gator_type()
            cog_data = pkt_cog.get_cog_data()
            ### Get user decision on handling data ###
            if selection_made is False:
                spinner.stop()
                get_input = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Print cog data? [y/n]{bcolors.ENDC}")
                if get_input == ("y" or "Y"):
                    selection_made = True
                    printout = True
                    print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Printing out cog data...{bcolors.ENDC}")
                elif get_input == ("n" or "N"):
                    selection_made = True
                    printout = False
                    print(f"{bsymbols.info} {bcolors.FAIL}Not printing cog data.{bcolors.ENDC}")
            if second_selection_made is False: 
                spinner.stop()
                second_get_input = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Read data to csv? [y/n]{bcolors.ENDC}")
                if second_get_input == ("y" or "Y"):
                    second_selection_made = True
                    save_to_csv = True
                    if os.path.exists(outputPath) and save_to_csv is True:
                        os.remove(outputPath)
                    print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Reading data to csv...{bcolors.ENDC}")
                elif second_get_input == ("n" or "N"):
                    second_selection_made = True
                    save_to_csv = False
                    print(f"{bsymbols.info} {bcolors.FAIL} Not reading to csv.{bcolors.ENDC}")
            if printout is True:
                print(f" Packet num: {bcolors.BOLD}{pkt_num}{bcolors.ENDC} ⇒ recorded at {bcolors.BOLD}{pkt_timestamp}ns{bcolors.ENDC} collection time. COG data ↴") #μ
                #print(f" DEBUG: Payload len: {pkt_payload_len} bytes | Gator type: {gator_type} | Gator version: {gator_version}") #Debug
                pretty(cog_data, 1)
                print(f" {bcolors.OKBLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{bcolors.ENDC}")
            #TODO: Save to CSV here!
            #------------------------------------------------------------------------------------------------------------------------------------------#
            if save_to_csv is True:
                #print(cog_data)
                for key, value in cog_data.items():
                    #print (key, value) #Debug
                    #print(type(value)) #Debug
                    bits = functools.reduce(lambda total, d: 10 * total + d, value, 0)
                    columns = {'Packet Num':[pkt_num],'Timestamp':[pkt_timestamp], 'Sensor Index': [key], 'Sensor Bits': [bits]}
                    frame = pd.DataFrame(columns)
                    frame.set_index('Packet Num', inplace=True)
                    data_frames.append(frame)
            #--------------------------------------------------------------------------------------------------------------------#        
        if save_to_csv is True:
            for frame in data_frames:
                #frame = pd.concat(frame, keys=["Packet number n"])
                frame.to_csv(outputPath, mode = 'a', header = not os.path.exists(outputPath))
        #Stop console status indicator
        error_check()
        spinner.stop()
        print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}") #Done
    except(KeyboardInterrupt, SystemExit):
        spinner.text_color = 'red'
        spinner.fail("mpg-foss: Process aborted.")
    return errorStatus

#Run the main function if this module is called directly.
if __name__ == '__main__':
   main()