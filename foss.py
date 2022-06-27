#!/usr/bin/env python
#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
import argparse
import subprocess
from scripts.fosmodule import bcolors, bsymbols, title

def handle_args():
    parser = argparse.ArgumentParser(description='Run foss.py help for more information. Run foss.py deps to install dependencies.')
    parser.add_argument('argument', type=str)
    args = parser.parse_args()
    return args

def switch(args):
    match args.argument:
        case "deps":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting dependency check tool...{bcolors.ENDC}")
            subprocess.call("python ./scripts/dependency-helper.py", shell=True)
            return
        case "data":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting gator-data collection tool...{bcolors.ENDC}")
            subprocess.call("python ./scripts/gator-data-to-csv.py", shell=True)
            return
        case "sim":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting gator-data simulator...{bcolors.ENDC}")
            subprocess.call("python ./scripts/gator-data-simulator.py", shell=True)
            return
        case "wisdom":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Providing you with design ethic...{bcolors.ENDC}")
            subprocess.call("python ./scripts/design-wisdom.py", shell=True)
            return
        case _:
            #launch help
            print(f"{bsymbols.info} {bcolors.FAIL}{bcolors.BOLD}mpg-foss: Unknown argument...{bcolors.ENDC}")
            print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Available commands:{bcolors.ENDC}")
            print(f"    deps{bcolors.ENDC}")
            print(f"    data{bcolors.ENDC}")
            print(f"    sim{bcolors.ENDC}")
            print(f"    wisdom{bcolors.ENDC}")
            return

#Run
args = handle_args()
title()
switch(args)

