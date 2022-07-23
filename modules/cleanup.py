#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#This script will clean the output folder.

import os
from formatmodule import bcolors, bsymbols
from halo import Halo

def main():
    spinner = Halo(spinner='dots')
    dir = "./data/out/"

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
    if erase_data == True:
        spinner.start()
        try:
            filelist = [f for f in os.listdir(dir) if f.endswith(".csv") ]
            for f in filelist:
                if f.find("example") == -1:
                    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Removing {f}...{bcolors.ENDC}")
                    os.remove(os.path.join(dir, f))
                    spinner.text_color = 'green'
                    spinner.succeed("mpg-foss: Success!")
            spinner.text_color = 'green'
            spinner.stop_and_persist(symbol='🗑️ '.encode('utf-8'), text=" mpg-foss: Done.")
        except:
            spinner.text_color = 'red'
            spinner.fail["mpg-foss: Unable to delete files, are they open elsewhere?"]
    exit()

#Run the main function if this module is called directly.
if __name__ == '__main__':
    main()