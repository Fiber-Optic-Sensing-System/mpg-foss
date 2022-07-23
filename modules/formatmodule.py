#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#Module to contain classes for mpg-foss.

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class bsymbols:
    info = '\U00002139'
    waste = '\U0001F5A9'

def title():
    print(f"{bcolors.OKGREEN}                                ____               {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}   ____ ___  ____  ____ _      / __/___  __________{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}  / __ `__ \/ __ \/ __ `/_____/ /_/ __ \/ ___/ ___/{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} / / / / / / /_/ / /_/ /_____/ __/ /_/ (__  |__  ) {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}/_/ /_/ /_/ .___/\__, /     /_/  \____/____/____/  {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}         /_/    /____/                             {bcolors.ENDC}")

class prints:

    #Prints items nicely.
    def pretty(self, d, indent=0):
        for key, value in d.items():
            print(' ' * indent + str(key), end='')
            if isinstance(value, dict):
                self.pretty(value, 0)
            else:
                print(f" ⇒ {bcolors.OKGREEN}{str(value)}{bcolors.ENDC}")
                
    #Prints items nicely in single line for nested lists.           
    def pretty_sl(self, d, indent=0):
        for key, value in d.items():
            print(' ' * indent + str(key) + ' ⇒ ', end='')
            if isinstance(value, dict):
                for k, v in value.items():
                    print(str(k) + ' ⇒ ', end='')
                    print(f"{bcolors.OKGREEN}{str(v)}{bcolors.ENDC} ", end='')
                if next(reversed(value.keys())) == k:
                    print()

class files:
    import os

    #Finds the next free path in an sequentially named list of files.
    def next_path(self, path_pattern):
        #e.g. path_pattern = 'file-%s.txt':
        i = 1
        #First do an exponential search
        while self.os.path.exists(path_pattern % i):
            i = i * 2

        #Result lies somewhere in the interval (i/2..i]
        a, b = (i // 2, i)
        while a + 1 < b:
            c = (a + b) // 2 # interval midpoint
            a, b = (c, b) if self.os.path.exists(path_pattern % c) else (a, c)
        return path_pattern % b
        

class zen:
    zen = [
    "Beautiful is better than ugly.",
    "Explicit is better than implicit.",
    "Simple is better than complex.",
    "Complex is better than complicated.",
    "Flat is better than nested.",
    "Sparse is better than dense.",
    "Readability counts.",
    "Special cases aren't special enough to break the rules.",
    "Although practicality beats purity.",
    "Errors should never pass silently.",
    "Unless explicitly silenced.",
    "In the face of ambiguity, refuse the temptation to guess.",
    "There should be one-- and preferably only one --obvious way to do it.",
    "Although that way may not be obvious at first unless you're Dutch.",
    "Now is better than never.",
    "Although never is often better than *right* now.",
    "If the implementation is hard to explain, it's a bad idea.",
    "If the implementation is easy to explain, it may be a good idea.",
    "Namespaces are one honking great idea -- let's do more of those!"]
