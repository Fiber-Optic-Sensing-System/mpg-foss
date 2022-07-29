"""
Written by Caleb C. & Andrew Valentini in 2022 for Carthage Space Sciences | WSGC | NASA
Collects data from the Gator hardware (or simulator) and saves it to a CSV file.
"""

from halo import Halo
from formatmodule import bcolors, bsymbols, prints, files
from fosmodule import datahelper, gatorpacket, packetsim
import pandas as pd
import os
import time

#Initialize
spinner = Halo(spinner='dots')
errorStatus = False
date = time.strftime("%Y-%m-%d")
f = files()
output_path = f.next_path(f"./data/out/{date}_run-%s.csv")
num_packets = 1
collectDuration = 0

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

def detect_gator():
    print(f"{bcolors.ENDC}{bsymbols.info} {bcolors.HEADER}mpg-foss: Searching for gator hardware...{bcolors.ENDC}")
    time.sleep(0.65)
    #Detect gator HW using pyusb
    return False

def main():
    #Globals
    global errorStatus
    global spinner
    global collectDuration
    global num_packets
    global output_path

    #Initialize
    spinner.start()
    data_frames = []

    #Try to detect hardware
    try:
        gator_found = detect_gator()
        if gator_found == False:
            print(f"{bsymbols.info} {bcolors.FAIL}mpg-foss: No gator hardware found!{bcolors.ENDC}")
            selection_pkts = False
            while selection_pkts == False:
                spinner.stop()
                get_input = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Num packets to sim? [int]{bcolors.ENDC}")
                get_input = get_input.strip()
                if get_input.isnumeric() == True:
                    num_packets = int(get_input)
                    selection_pkts = True
                else:
                    print(f"{bsymbols.info} {bcolors.FAIL}Enter an integer value!{bcolors.ENDC}")
            spinner.start()
        else:
            #Collect real gator data into buffer.
            pass
    except(KeyboardInterrupt, SystemExit):
        spinner.text_color = 'red'
        spinner.fail("mpg-foss: Process aborted.")

    #Move on to data collection
    try:
        #Init console status indicator
        ### Instantiate classes ###
        datum = datahelper()
        simpacket = packetsim()
        pprint = prints()
        #-------------------------#
        #Set print option
        selection_print = False
        printout = False
        selection_csv = False
        save_to_csv = False
        strain_selection = False
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
            #pkt_payload_len = pkt_header.get_payload_len()
            #gator_version = pkt_header.get_version()
            #gator_type = pkt_header.get_gator_type()
            cog_data = pkt_cog.get_cog_data()
            strain_data = pkt_cog.get_strain_data()
            ### Get user decision on handling data ###
            if strain_selection is False: 
                spinner.stop()
                get_input1 = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Covert CoG data to Strain? [y/n]{bcolors.ENDC}") 
                if get_input1 == ("y" or "Y"):
                    strain_selection = True
                    selection_print = True
                    print(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Coverting CoG data to Strain...{bcolors.ENDC}")
                elif get_input1 == ("n" or "N"):
                    strain_selection = False
                    selection_print = True 
                    print(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Reading data as central wavelength CoG bits...{bcolors.ENDC}")
            if selection_print is False:
                spinner.stop()
                get_input2 = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Print cog data? [y/n]{bcolors.ENDC}")
                if get_input2 == ("y" or "Y"):
                    selection_print = True
                    printout = True
                    print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Printing out cog data...{bcolors.ENDC}")
                elif get_input2 == ("n" or "N"):
                    selection_print = True
                    printout = False
                    print(f"{bsymbols.info} {bcolors.FAIL}Not printing cog data.{bcolors.ENDC}")
            if selection_csv is False:
                spinner.stop()
                get_input3 = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Write data to csv? [y/n]{bcolors.ENDC}")
                if get_input3 == ("y" or "Y"):
                    selection_csv = True
                    save_to_csv = True
                    if os.path.exists(output_path) and save_to_csv is True:
                        os.remove(output_path)
                    print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Writing data to csv...{bcolors.ENDC}")
                elif get_input3 == ("n" or "N"):
                    selection_csv = True
                    save_to_csv = False
                    print(f"{bsymbols.info} {bcolors.FAIL} Not reading to csv.{bcolors.ENDC}")
            if printout and strain_selection is True:
                print(f" Packet num: {bcolors.BOLD}{pkt_num}{bcolors.ENDC} ⇒ recorded at {bcolors.BOLD}{pkt_timestamp:.4f}μs{bcolors.ENDC} collection time. Strain data ↴")
                #print(f" DEBUG: Payload len: {pkt_payload_len} bytes | Gator type: {gator_type} | Gator version: {gator_version}") #Debug
                #Pretty printing of cog data
                pprint.pretty_sl(strain_data, 1)
                print(f" {bcolors.OKBLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{bcolors.ENDC}")
            if printout is True and strain_selection is False:
                print(f" Packet num: {bcolors.BOLD}{pkt_num}{bcolors.ENDC} ⇒ recorded at {bcolors.BOLD}{pkt_timestamp:.4f}μs{bcolors.ENDC} collection time. CoG data ↴")
                #print(f" DEBUG: Payload len: {pkt_payload_len} bytes | Gator type: {gator_type} | Gator version: {gator_version}") #Debug
                #Pretty printing of cog data
                pprint.pretty_sl(cog_data, 1)
                print(f" {bcolors.OKBLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{bcolors.ENDC}")
            #TODO: Save to CSV here!
            #------------------------------------------------------------------------------------------------------------------------------------------#
            if save_to_csv and strain_selection is True:
                spinner.start()
                cog = {}
                err = {}
                for key, value in cog_data.items():
                    for k, v in value.items():
                        if k == "cog":
                            cog[key] = v
                        elif k == "err":
                            err[key] = v
                for key, value in cog_data.items():
                    columns = {'packet':[pkt_num],'timestamp':[pkt_timestamp], 'sensor': [key], 'cog': [cog[key]], 'err': [err[key]]}
                    frame = pd.DataFrame(columns)
                    frame.set_index('packet', inplace=True)
                    data_frames.append(frame)
            if save_to_csv is True and strain_selection is False:
                spinner.start()
                cog = {}
                err = {}
                for key, value in cog_data.items():
                    for k, v in value.items():
                        if k == "cog":
                            cog[key] = v
                        elif k == "err":
                            err[key] = v
                for key, value in cog_data.items():
                    columns = {'packet':[pkt_num],'timestamp':[pkt_timestamp], 'sensor': [key], 'cog': [cog[key]], 'err': [err[key]]}
                    frame = pd.DataFrame(columns)
                    frame.set_index('packet', inplace=True)
                    data_frames.append(frame)
            #--------------------------------------------------------------------------------------------------------------------#
        if save_to_csv is True:
            for frame in data_frames:
                #frame = pd.concat(frame, keys=["Packet number n"])
                frame.to_csv(output_path, mode = 'a', header = not os.path.exists(output_path))
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