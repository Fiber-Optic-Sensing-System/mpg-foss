#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#This script will clean the output folder.

import os
from formatmodule import bcolors, bsymbols
from halo import Halo

def main():
    spinner = Halo(spinner='dots')
    dir = "../out"

    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: This will remove data from previous runs...{bcolors.ENDC}")

    erase_data = False
    spinner.stop()
    get_input = input(f"{bsymbols.info} {bcolors.OKCYAN}mpg-foss: Are you sure? [y/n]{bcolors.ENDC}")
    get_input = get_input.strip()
    if get_input == "y" or get_input == "Y":
        erase_data = True
    else:
        print(f"{bsymbols.info} {bcolors.FAIL}mpg-foss: Aborting ...{bcolors.ENDC}")
        exit()

    spinner.start()
    if erase_data == True:
        try:
            filelist = [f for f in os.listdir(dir) if f.endswith(".csv") ]
            for f in filelist:
                if f.find("example") == -1:
                    os.remove(os.path.join(dir, f))
            spinner.symbol = "🗑️"
            spinner.succeed("mpg-foss: Success!")
        except:
            print(f"{bsymbols.info} {bcolors.FAIL}mpg-foss: Unable to delete files, are they open elsewhere?{bcolors.ENDC}")
            exit()

#Run the main function if this module is called directly.
if __name__ == '__main__':
    main()