#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#Simulates gator data for the purposes of testing.
from fosmodule import bcolors, bsymbols 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.api as sm 
print(f"{bsymbols.info} {bcolors.FAIL}{bcolors.BOLD}mpg-foss: Not implemented yet!{bcolors.ENDC}")

#ensuring the reproducibility of data values
np.random.seed(1)

time_samples = 5000
time_series = np.random.normal(size = time_samples)

#creating the plot 
plt.figure(figsize=(10,5))
plt.plot(time_series[0:1000])
#saving the generated graph as a .png file
plt.savefig('white_noise.png')

#converting time series to pandas objects 
time_series_pd = pd.Series(time_series)



