#Written by Caleb C. & Andrew V. in 2022 for Carthage Space Sciences | WSGC | NASA
#Simulates gator data for the purposes of testing.
from fosmodule import bcolors, bsymbols 
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

#ensuring the reproducibility of data values
np.random.seed(1)

time_samples = 5000
time_series = np.random.normal(size = time_samples)

#creating the plot 
try:
  plt.figure(figsize=(10,5))
  plt.plot(time_series[0:1000])
  #saving the generated graph as a .png file
  plt.savefig('./data/images/white_noise.png')
except:
  fail = True

#converting time series to pandas objects 
time_series_pd = pd.Series(time_series)

#Applying the Fourier Transform 
time_series_fft = fft(time_series)
try:
  plt.figure(figsize=(10,5))
  plt.plot(time_series_fft[0:1000])
  plt.savefig('./data/images/fft_white_noise.png')
except:
  fail = True

#done
if fail != True:
    spinner.text_color = 'green'
    spinner.succeed("mpg-foss: Success.")
    print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")
else:
    spinner.text_color = 'red'
    spinner.fail("mpg-foss: There was an exception!")
    print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")



