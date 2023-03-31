#!/usr/bin/env python
#Written by Caleb C. in 2023 for Carthage Space Sciences | WSGC | NASA
import sys
#Check Interpreter Version
if sys.version_info < (3, 10):
    print("\033[91m\U00002717 \033[91m\033[1mmpg-foss: Python version 3.10 or newer is required to run this program!\033[0m")
    print(f"\033[94m\U00002139 \033[94m\033[1mmpg-foss: Your current Python version is {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\033[0m")
    exit(1)
import subprocess
subprocess.call(f"python foss_start.py {sys.argv[1]}", shell=True)