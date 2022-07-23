#!/usr/bin/env python
#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
import argparse
import subprocess
from modules.formatmodule import bcolors, bsymbols, prints

def handle_args():
    parser = argparse.ArgumentParser(description='Run foss.py help for more information. Run foss.py deps to install dependencies.')
    parser.add_argument('argument', type=str)
    args = parser.parse_args()
    return args

def switch(args):
    match args.argument:
        case "deps" | "dependencies" | "update":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting dependency check tool...{bcolors.ENDC}")
            subprocess.call("python ./modules/dependency-helper.py", shell=True)
            return
        case "data" | "d" | "collect":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting gator-data collection tool...{bcolors.ENDC}")
            subprocess.call("python ./modules/gator-data-to-csv.py", shell=True)
            return
        case "sim":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Starting gator-data simulator...{bcolors.ENDC}")
            subprocess.call("python ./modules/gator-data-simulator.py", shell=True)
            return
        case "clean" | "cleanup" | "remove":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Clean output directory...{bcolors.ENDC}")
            subprocess.call("python ./modules/cleanup.py", shell=True)
            return
        case "wisdom" | "zen":
            print(f"{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}mpg-foss: Providing you with design ethic...{bcolors.ENDC}")
            subprocess.call("python ./modules/design-wisdom.py", shell=True)
            return
        case _:
            #launch help
            print(f"{bsymbols.info} {bcolors.FAIL}{bcolors.BOLD}mpg-foss: Unknown argument...{bcolors.ENDC}")
            print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Available commands:{bcolors.ENDC}")
            print(f"    deps{bcolors.ENDC}")
            print(f"    data{bcolors.ENDC}")
            print(f"    clean{bcolors.ENDC}")
            print(f"    sim{bcolors.ENDC}")
            print(f"    wisdom{bcolors.ENDC}")
            return

#Run
p = prints()
args = handle_args()
p.title()
switch(args)

