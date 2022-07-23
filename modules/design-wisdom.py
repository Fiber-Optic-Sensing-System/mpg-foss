#This scrpt prints the zen of python by Tim Peters.
#Also accessable by 'import this'
#The zen array of strings in fosmodule can be used for testing purposes.
import time
from halo import Halo
from formatmodule import bcolors, zen

spinner = Halo(spinner='dots')
try:
    print(f"{bcolors.OKCYAN}{bcolors.BOLD}The Zen of Python, by Tim Peters{bcolors.ENDC}")
    time.sleep(0.75)
    for line in zen.zen:
      spinner.start(line)
      time.sleep(0.75)
      spinner.succeed()
    spinner.stop()
except (KeyboardInterrupt, SystemExit):
    spinner.stop()