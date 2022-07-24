# -*- coding: utf-8 -*-
#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#This script will get the dependencies for fossS/MPG related Python projects and self update from the repo.
import sys, subprocess
from formatmodule import bcolors, bsymbols

modules_base = ['wheel', 'halo', 'GitPython']
modules_dependencies = ['struct', 'pyusb', 'pandas', 'bitarray']
modules_alt_name = {'GitPython': 'git', 'pyusb': 'usb.core'}
project_url = "https://github.com/Fiber-Optic-Sensing-System/mpg-foss.git"
fail = False
spinner = None

def basic():
    global modules_base
    print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.HEADER} mpg-foss: Checking dependencies.{bcolors.ENDC}")
    for module in modules_base:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__ (module_alt)
            else:
                __import__ (module)
        except ImportError:
            print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.ENDC} mpg-foss: {module} not found...")
            print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.HEADER} mpg-foss: Installing {module}...{bcolors.ENDC}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.SubprocessError:
                print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} mpg-foss: Could not acquire module named {module}. {bcolors.ENDC}")

def check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    except subprocess.SubprocessError:
        print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} mpg-foss: Could not update pip...{bcolors.ENDC}")

def self_update():
    try:
        import git
        spinner.text_color ='magenta'
        spinner.info("mpg-foss: Performing self update...")
        spinner.start()
        g = git.cmd.Git(project_url)
        msg = g.pull()
        tag = subprocess.check_output(["git", "describe", "--always"]).strip().decode()
        spinner.text_color ='magenta'
        spinner.info(f"git: Latest commit to this branch was {tag}")
        spinner.start()
        spinner.info(f"{msg}")
        spinner.start()
    except (git.exc.GitCommandError, subprocess.SubprocessError):
        spinner.text_color ='red'
        spinner.fail("mpg-foss: Could not update from git.")

def advanced():
    global modules_dependencies
    for module in modules_dependencies:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__ (module_alt)
            else:
                __import__ (module)
        except ImportError:
            spinner.text_color ='grey'
            spinner.fail(f"mpg-foss: {module} not found...")
            spinner.start()
            spinner.text_color ='magenta'
            spinner.info(f"mpg-foss: Installing {module}...")
            spinner.start()
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.SubprocessError:
                spinner.text_color ='red'
                spinner.fail(f"mpg-foss: Could not acquire module named {module}.")

def test(mode):
    global modules_dependencies
    global modules_base
    global modules_alt_name
    global fail
    if mode == 'basic':
        print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.HEADER} mpg-foss: Verifying...{bcolors.ENDC}")
        for module in modules_base:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__ (module)
            except ImportError:
                fail = True
                print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} mpg-foss: {module} was not imported. Try manually installing it. {bcolors.ENDC}")
    elif mode == 'advanced':
        spinner.text_color ='magenta'
        spinner.info("mpg-foss: Verifying...")
        spinner.start()
        for module in modules_dependencies:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__ (module)
            except ImportError:
                fail = True
                spinner.text_color ='red'
                spinner.fail(f"mpg-foss: {module} was not imported. Try manually installing it.")
    check_fail()

def init_spinner():
    global spinner
    from halo import Halo
    spinner = Halo(spinner='dots', animation='bounce')
    spinner.start()

def check_fail():
    global fail
    global spinner
    if fail is not True and spinner is not None:
        spinner.text_color = 'green'
        spinner.succeed(" mpg-foss: Dependencies present & checked.")
        spinner.info("mpg-foss: Done.")
    elif fail is True:
        if spinner is not None:
            spinner.text_color = 'red'
            spinner.fail(" mpg-foss: Some tests failed!")
        else:
            print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} mpg-foss: Some tests failed!{bcolors.ENDC}")

def main():
    try:
        check_pip()
        basic()
        test('basic')
        init_spinner()
        self_update()
        advanced()
        test('advanced')
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    sys.exit(0)

#Run the main function if this module is called directly.
if __name__ == '__main__':
    main()