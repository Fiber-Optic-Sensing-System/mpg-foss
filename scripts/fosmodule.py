#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#Module to contain classes for mpg-foss.
import struct

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

def title():
    print(f"{bcolors.OKGREEN}                                ____               {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}   ____ ___  ____  ____ _      / __/___  __________{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}  / __ `__ \/ __ \/ __ `/_____/ /_/ __ \/ ___/ ___/{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} / / / / / / /_/ / /_/ /_____/ __/ /_/ (__  |__  ) {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}/_/ /_/ /_/ .___/\__, /     /_/  \____/____/____/  {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}         /_/    /____/                             {bcolors.ENDC}")

class GatorPacket:
    class header:
        def __init__(self):
            self._len = 16
            self._data: bytearray

        @property
        def len(self):
            return self._len

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, data: bytearray):
            if not isinstance(data, bytearray):
                raise TypeError("Data input must be a bytearray.")
            self._data = data

        def get_payload_len(self):
            decode = self._data[0:4]
            result, = struct.unpack('>I', decode)
            return int(result) #Size in bytes?

        def get_timestamp(self):
            decode = self._data[4:8]
            result, = struct.unpack('>I', decode)
            return int(result) #Time since epoch

        def get_packet_num(self):
            decode = self._data[8:10]
            result, = struct.unpack('>H', decode)
            return int(result) #This packet number

        def get_gator_type(self):
            decode = self._data[10]
            decode = decode.to_bytes(1, byteorder='big')
            result, = struct.unpack('>B', decode)
            return int(result) #The type of gator connected

        def get_version(self):
            decode = self._data[11]
            decode = decode.to_bytes(1, byteorder='big')
            result, = struct.unpack('>B', decode)
            return int(result) #Gator firmware version

        #TODO: Needs changes 
        def get_sync_status(self):
            synced = False
            yoho = 'yoho'
            decode = self._data[12:16]
            decode = bytes(decode)
            result, = struct.unpack('>s', decode)
            if str(result) == yoho:
                synced = True
            return synced #Returns true if synced.

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
