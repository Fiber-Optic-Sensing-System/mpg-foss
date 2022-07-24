#Written by Caleb C. & Andrew V. in 2022 for Carthage Space Sciences | WSGC | NASA
#Simulates gator data at the hardware (USB) level for the purposes of testing.
from formatmodule import bcolors, bsymbols

from halo import Halo
fail = False
spinner = Halo(spinner='dots')
spinner.start()
print(f"{bsymbols.info} {bcolors.FAIL}{bcolors.BOLD}mpg-foss: Not fully implemented yet!{bcolors.ENDC}")

#done
if fail != True:
    spinner.text_color = 'green'
    spinner.succeed("mpg-foss: Success.")
    print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")
else:
    spinner.text_color = 'red'
    spinner.fail("mpg-foss: There was an exception!")
    print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")