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
        import wheel
    except ImportError:
        print(f"{bcolors.OKCYAN}mpg-foss: wheel not found...{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}mpg-foss: installing wheel...{bcolors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'wheel'])
    try:
        import halo
    except ImportError:
        print(f"{bcolors.OKCYAN}mpg-foss: halo not found...{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}mpg-foss: installing halo...{bcolors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'halo'])
    pass

def advanced():
    try:
        import usb.core
    except ImportError:
        print(f"{bcolors.OKCYAN}mpg-foss: pyusb not found...{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}mpg-foss: installing pyusb...{bcolors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyusb'])
    try:
        import pandas
    except ImportError:
        print(f"{bcolors.OKCYAN}mpg-foss: pandas not found...{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}mpg-foss: installing pandas...{bcolors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
    """
    try:
        import ttkbootstrap
    except ImportError:
        print(f"{bcolors.OKCYAN}mpg-foss: ttkbootstrap not found...{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}mpg-foss: installing ttkbootstrap...{bcolors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'ttkbootstrap'])
    """
    pass

def test():
    print(f"{bcolors.HEADER}mpg-foss: Verifying...{bcolors.ENDC}")
    try:
        import wheel
    except ImportError:
        fail = True
        print(f"{bcolors.FAIL}mpg-foss: Could not import wheel. Try manually installing it. {bcolors.ENDC}")
    try:
        import halo
    except ImportError:
        fail = True
        print(f"{bcolors.FAIL}mpg-foss: Could not import halo. Try manually installing it. {bcolors.ENDC}")
    try:
        import usb.core
    except ImportError:
        fail = True
        print(f"{bcolors.FAIL}mpg-foss: Could not import pyusb. Try manually installing it. {bcolors.ENDC}")
    try:
        import pandas
    except ImportError:
        fail = True
        print(f"{bcolors.FAIL}mpg-foss: Could not import pandas. Try manually installing it. {bcolors.ENDC}")
    """
    try:
        import ttkbootstrap
    except ImportError:
        fail = True
        print(f"{bcolors.FAIL}mpg-foss: Could not import ttkbootstrap. Try manually installing it. {bcolors.ENDC}")
    """
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