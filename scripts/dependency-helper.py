# -*- coding: utf-8 -*-
#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#This script will get the dependencies for fossS/MPG related Python projects.
import subprocess
import sys
from fosmodule import bcolors, bsymbols

fail = False

def basic():
    print(f"{bsymbols.info} {bcolors.HEADER}mpg-foss: Checking dependencies.{bcolors.ENDC}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    except subprocess.SubprocessError:
        print(f"{bcolors.OKCYAN}mpg-foss: could not update pip...{bcolors.ENDC}")

    installations = ['wheel', 'halo']

    for installation in installations:
        try:
            __import__ (installation)
        except ImportError:
            print(f"{bcolors.OKCYAN}mpg-foss: {installation} not found...{bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}mpg-foss: installing {installation}...{bcolors.ENDC}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", installation])
    
    pass

def advanced():

    dependencies = ['struct', 'usb.core', 'pandas', 'matplotlib', 'statsmodels', 'ttkbootstrap']

    for dependency in dependencies:
        try:
            
            __import__ (dependency)
        except ImportError:
            print(f"{bcolors.OKCYAN}mpg-foss: {dependency} not found...{bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}mpg-foss: installing {dependency}...{bcolors.ENDC}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])

    pass

def test():
    print(f"{bcolors.HEADER}mpg-foss: Verifying...{bcolors.ENDC}")

    graphics = ['halo', 'struct', 'usb.core', 'pandas', 'matplotlib', 'statsmodels', 'ttkbootstrap']
    
    for graphic in graphics:
        try:
            __import__ (graphic)
        except ImportError:
            fail = True
            print(f"{bcolors.FAIL}mpg-foss: Could not import {graphic}. Try manually installing it. {bcolors.ENDC}")
    
    pass

try:
    basic()
    from halo import Halo
    spinner = Halo(spinner='dots')
    spinner.start()
    advanced()
    test()
    if fail != True:
        spinner.text_color = 'green'
        spinner.succeed("mpg-foss: Dependencies present & checked.")
        print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")
    else:
        spinner.text_color = 'red'
        spinner.fail("mpg-foss: Some tests failed!")
        print(f"{bsymbols.info} {bcolors.OKGREEN}mpg-foss: Done.{bcolors.ENDC}")
except (KeyboardInterrupt, SystemExit):
    spinner.stop()