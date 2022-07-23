#Written by Caleb C. & Andrew V. in 2022 for Carthage Space Sciences | WSGC | NASA
#Simulates gator data for the purposes of testing.
from formatmodule import bcolors, bsymbols
import struct
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.api as sm 
from scipy.fft import fft

#TODO: Check if noise is being generated correctly.
#TODO: Covert noise to data in gator format and transmit.

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



