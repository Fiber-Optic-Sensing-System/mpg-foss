#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#Module to contain classes for mpg-foss.
#from bitarray import bitarray

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
        import struct
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
            result, = self.struct.unpack('>I', decode)
            return int(result) #Size in bytes?

        def get_timestamp(self):
            decode = self._data[4:8]
            result, = self.struct.unpack('>I', decode)
            return int(result) #Time since epoch

        def get_packet_num(self):
            decode = self._data[8:10]
            result, = self.struct.unpack('>H', decode)
            return int(result) #This packet number

        def get_gator_type(self):
            decode = self._data[10]
            decode = decode.to_bytes(1, byteorder='big')
            result, = self.struct.unpack('>B', decode)
            return int(result) #The type of gator connected

        def get_version(self):
            decode = self._data[11]
            decode = decode.to_bytes(1, byteorder='big')
            result, = self.struct.unpack('>B', decode)
            return int(result) #Gator firmware version
        
        def get_characters(self):
            status = False
            characters = [12, 13, 14, 15]
            yoho = "ohoy"
            sync_str = ""
            for character in characters:
                char = chr(self._data[character])
                sync_str += char
            if yoho == sync_str:
                status = True
            return status
  

    class Status:
        import struct
        def __init__(self):
            self._len = 3
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

        def get_num_found(self):
            decode = self._data[17:20]
            result, = self.struct.unpack('>c', decode)
            return int(result) 

    class data: 
        def __init__(self):
            self._len = 23
            self._data: bytearray
            self._num_sensors = 8

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

        def access_bit(self, data, num):
            base = int(num // 8)
            shift = int(num % 8)
            return (data[base] >> shift) & 0x1

        def sort(buffer, somepacket, somedata, payloadDict):
            ret_val = -1
            i = -1 
            is_sync = False
            while (not is_sync and i < len(buffer)):
                if buffer[i] == 'y' and buffer[i+1] == 'o' and buffer[i+2] == 'h' and buffer[i+3] == 'o':
                    is_sync = True
                    ret_val = i - 15
                else:
                    i = i + 4
                    
            if is_sync == False: 
                print("yoho not found")
            #print(i)
            print(ret_val, "This is ret val")
            payload_beginning = i - 27
            payload_end = somepacket.get_payload_len() 
            payloadDict.update({somepacket.get_packet_num(): somedata[payload_beginning:payload_end]})
            timestamp_beginning = ret_val + 1
            timestamp_end = somepacket.get_timestamp() + timestamp_beginning
            return ret_val, payload_beginning, payload_end, timestamp_beginning, timestamp_end

        def sortcog(timestamp, payload_beginning, payload_end, lis, somedata, cog_data_dict):
            value2 = 0 
            if value2 < len(lis):
                cog_data_beginning = payload_beginning + 3
                cog_data_end = payload_beginning + 27
                if (cog_data_end == payload_end): 
                    some_data_slice = somedata[cog_data_beginning:cog_data_end]
                    cog_data_dict[timestamp] = some_data_slice
                return cog_data_beginning, cog_data_end
            else: 
                value2 = value2 + 1

        def get_cog_data(self): 
            decode = self._data[20:44]
            as_string = bytes(decode)
            #print(as_string)
            bytes_as_bits = [self.access_bit(decode, i) for i in range (len(decode)*8)]
            #print(bytes_as_bits)
            #print("Length: ", len(bytes_as_bits))
            sensors = []
            for sensor in range(self._num_sensors):
                x = 0
                y = 19
                sensors.append(bytes_as_bits[x:y])
                x += 19
                y += 19
            return sensors

#This class is used for generating fake gator packets.
class packetsim:
    import struct
    import time
    import bitarray
    import random
    def __init__(self):
        self._num_sensors = 8
        self._packet_num = 0
        self._timestamp = 0
        self._payload_size = 27
        self._header = {
            "yoho": "yoho",
            "version": 0,
            "type": 1,
        }
        self._status = {

        }
        self._cog_data = {

        }

    def generate_status_word(self):
        status_word = self.bitarray.bitarray(24)
        status_word.setall(0)
        #Bit at 0 appears to always be one.
        status_word[0] = 1
        #Bit at 4 should be 1 for 0b1000 aka 8
        status_word[4] = 1
        #Set bits 5-12 to 1 for sensorx OK status
        for i in range(7):
            status_word[i+5] = 1
        #Set temp ok to 1
        status_word[13] = 1
        #Set bits 14-18 to rand for sequence num
        for i in range(4):
            status_word[i+14] = self.random.randint(0, 1)
        retval = bytearray()
        retval.extend(status_word.tobytes())
        return retval

    def generate_cog_data(self):
        #24 bytes of data
        retval = bytearray()
        for sensor in range(8):
            cog_data = self.bitarray.bitarray(24)
            cog_data.setall(0)
            #Sensor data 0-17 random bits
            for bit in range(17):
                cog_data[bit] = self.random.randint(0, 1)
            #Set sensor error to 0
            cog_data[18] = 0
            retval.extend(cog_data.tobytes())
        return retval

    #Adds one to the packet number and returns it.
    def get_and_incriment_pkt(self):
        self._packet_num += 1
        return self._packet_num

    #Gets the program time and returns it as a float.
    def create_and_get_timestamp(self):
        self._timestamp = self.time.perf_counter()
        return self._timestamp

    #Returns the size of the packet payload in bytes.
    def get_payload_size(self):
        return self._payload_size

    #Helper function to pack strings.
    def string_packer(self, string):
        string = bytes(string, 'utf-8')
        retval = self.struct.pack('>{}s'.format(len(string)), string)
        return retval
    
    #Generates a single packet.
    def generate_packet(self):
        #Create byte array of raw simulated data.
        raw_packet = bytearray()
        #Add dynamic/generated values to header.
        self._header["pkt_num"] = self.get_and_incriment_pkt()
        self._header["timestamp"] = self.create_and_get_timestamp()
        self._header["payload_size"] = self.get_payload_size()
        self._status["sensor_status"] = self.generate_status_word()
        self._cog_data["cog_data"] = self.generate_cog_data()
        #Add the yoho value to the packet.
        intermediate = self.string_packer(self._header.get('yoho'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the version number to the packet.
        intermediate = self.struct.pack('>B', self._header.get('version'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the type number to the packet.
        intermediate = self.struct.pack('>B', self._header.get('type'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the packet number to the packet.
        intermediate = self.struct.pack('>H', self._header.get('pkt_num'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the time stamp to the packet.
        intermediate = self.struct.pack('>f', self._header.get('timestamp'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the payload size to the packet.
        intermediate = self.struct.pack('>I', self._header.get('payload_size'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the status word to the packet.
        intermediate = self._status.get('sensor_status')
        for byte in intermediate : raw_packet.append(byte)
        #Add the cog data to the packet.
        intermediate = self._cog_data.get('cog_data')
        for byte in intermediate : raw_packet.append(byte)
        #Return the generated packet.
        return raw_packet

    #This function will generate a specified number of random gator packets.
    def generate_packets(self, num_packets):
        #Create byte array of raw simulated data.
        raw_packets = bytearray()
        #Generate the specified number of packets.
        for i in range(num_packets):
            raw_packets.extend(self.generate_packet())
        #Return the generated packets.
        return raw_packets
            
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
