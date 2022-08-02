#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#Module to contain classes for mpg-foss.

class datahelper:
    import re
    def __init__(self):
        self._header_indexes = {}
        self._packets = {}
        self._raw_data: bytearray

    @property
    def header_indexes(self):
        return self._header_indexes

    @property
    def packets(self):
        return self._packets

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, data_in: bytearray):
        if not isinstance(data_in, bytearray):
            raise TypeError("Data input must be a bytearray.")
        self._raw_data = data_in

    #Finds the index of each packet in the raw data.
    def sort(self):
        #Get raw data object
        data = self.raw_data
        if self.raw_data is not None:
            #Use regex to find all packets.
            hit_num = 0
            #For reference, yoho(ohoy here, because big endian) is b'\x6f\x68\x6f\x79'
            for match in self.re.finditer(b'\x6f\x68\x6f\x79',data):
                self._header_indexes[hit_num] = match.end() - 16 #Subtract 16 to reach beginning of packet.
                hit_num += 1 #Post increment
        return self._header_indexes

    def parse(self):
        #Get packets object
        packets = self.packets
        indexes = self.header_indexes
        indexes = self.sort()
        packets.clear()
        keys = indexes.keys()
        for key in keys:
            packets[key] = self.raw_data[indexes[key]:indexes[key]+43]
        return packets

class gatorpacket:
    def __init__(self):
        self._raw_data: bytearray
        self._header_instance: gatorpacket.header
        self._status_instance: gatorpacket.status
        self._data_instance: gatorpacket.data

    def create_inner(self):
        self._header_instance = gatorpacket.header(self)
        self._status_instance = gatorpacket.status(self)
        self._data_instance = gatorpacket.data(self)
        return self._header_instance, self._status_instance, self._data_instance

    @property
    def header_instance(self):
        return self._header_instance

    @property
    def status_instance(self):
        return self._status_instance

    @property
    def data_instance(self):
        return self._data_instance

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, data_in: bytearray):
        if not isinstance(data_in, bytearray):
            raise TypeError("Data input must be a bytearray.")
        self._raw_data = data_in

    class header:
        import struct
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self._len = 16

        @property
        def len(self):
            return self._len

        def get_payload_len(self):
            decode = self.outer_instance.raw_data[0:4]
            result, = self.struct.unpack('>I', decode)
            return int(result) #Size in bytes?

        def get_timestamp(self):
            decode = self.outer_instance.raw_data[4:8]
            result, = self.struct.unpack('>f', decode)
            return float(result) #Time since epoch

        def get_packet_num(self):
            decode = self.outer_instance.raw_data[8:10]
            result, = self.struct.unpack('>H', decode)
            return int(result) #This packet number

        def get_gator_type(self):
            decode = self.outer_instance.raw_data[10]
            decode = decode.to_bytes(1, byteorder='big')
            result, = self.struct.unpack('>B', decode)
            return int(result) #The type of gator connected

        def get_version(self):
            decode = self.outer_instance.raw_data[11]
            decode = decode.to_bytes(1, byteorder='big')
            result, = self.struct.unpack('>B', decode)
            return int(result) #Gator firmware version

        def get_characters(self):
            status = True
            characters = [12, 13, 14, 15]
            yoho = "ohoy"
            sync_str = ""
            for character in characters:
                char = chr(self.outer_instance.raw_data[character])
                sync_str += char
            if yoho == sync_str:
                status = True
            return status

    class status:
        import struct
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self._len = 3

        @property
        def len(self):
            return self._len

        def get_num_found(self):
            decode = self.outer_instance.raw_data[17:20]
            result, = self.struct.unpack('>c', decode)
            return int(result)

    class data:
        import struct
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self._len = 24
            self._num_sensors = 8
            self._cog_dictionary = {}
            self._sensors = {}

        @property
        def cog_dictionary(self):
            return self._cog_dictionary

        @property
        def len(self):
            return self._len

        def get_cog_data(self):
            decode = self.outer_instance.raw_data[19:len(self.outer_instance.raw_data)]
            pad_text = lambda i: "0" if i < 10 else ""
            bits = []

            for byte in decode:
                for bit in reversed(range(8)):
                    bits.append(((byte >> bit) & 1))

            sensor_index = 0
            bit_string = ""
            for index, bit in enumerate(bits):
                if index < 152:
                    bit_string += str(bit)
                    if len(bit_string) == 18:
                        sensor_index += 1
                        self._sensors[f"sensor_{pad_text(sensor_index)}{sensor_index}"] = {}
                        self._sensors[f"sensor_{pad_text(sensor_index)}{sensor_index}"]['cog'] = bit_string
                        bit_string = ""
                    if index % 19 == 18:
                        bit_string = str(bit)
                        self._sensors[f"sensor_{pad_text(sensor_index)}{sensor_index}"]['err'] = bit_string
                        bit_string = ""
            return self._sensors
        def get_strain_data(self):
            strain_string = self._sensors["sensor_01"].get('cog')
            strain_value = int(strain_string, 2)
            #print(cog_string, "This is cog string")
            #print(cog_value, "This is cog value")
            #converting the defalt cog data bits into central wavelengths 
            wavelengths = (1514 + strain_value) / ((2 ** 18)*72)
            #The defalt central wavelength is that when the FBGs have undergone no strain or temperature difference(setting this as a constant for now; this will have to be experimentally determined later)
            default_cw = 1500
            therm_expan_coef = 25.5
            #thermo_optic_coef could not be found online...guessing here
            thermo_optic_coef = 25.5
            delta_temp = 0
            #the strain optic coeffecient for a glass fiber is given as .22 in the User's Manual
            strain_optic_coefficent = .22
            strain = (((wavelengths-default_cw)/default_cw) - ((therm_expan_coef - thermo_optic_coef) * delta_temp)) / (1 - strain_optic_coefficent)
            #print(strain, "This is strain")
            return strain
#This class is used for generating fake gator packets.
class packetsim:
    import struct
    import bitarray
    import random
    def __init__(self):
        self._on_init = False
        self._num_sensors = 8
        self._packet_num = 0
        self._timestamp = 0
        self._payload_size = 27
        self._header = {
            "yoho": "ohoy",
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
        cog_bits = self.bitarray.bitarray(184)
        #Set all bits to 0
        cog_bits.setall(0)
        #150 is the end of the cog data

        #Set bits 0-151 to 1 or 0 randomly
        for i in range(151):
            cog_bits[i] = self.random.randint(0, 1)

        #Set last 4 sensors to 0 to simulate none connected
        cog_bits[76:151] = 0

        #Set error status bits
        cog_bits[18] = 0
        cog_bits[37] = 0
        cog_bits[56] = 0
        cog_bits[75] = 0
        cog_bits[94] = 1
        cog_bits[113] = 1
        cog_bits[132] = 1
        cog_bits[151] = 1

        #Add data to padding bits
        cog_bits[152:184] = 1

        #Convert bitfield to bytes
        retval = cog_bits.tobytes()

        return retval

    #Adds one to the packet number and returns it.
    def get_and_incriment_pkt(self):
        self._packet_num += 1
        return self._packet_num

    #Gets the program time and returns it as a float.
    def create_and_get_timestamp(self):
        if self._on_init is False:
            self._on_init = True
            self._timestamp = self.random.random()
        else:
            self._timestamp += 0.025
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
        #Add the payload size to the packet.
        intermediate = self.struct.pack('>I', self._header.get('payload_size'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the time stamp to the packet.
        intermediate = self.struct.pack('>f', self._header.get('timestamp'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the packet number to the packet.
        intermediate = self.struct.pack('>H', self._header.get('pkt_num'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the type number to the packet.
        intermediate = self.struct.pack('>B', self._header.get('type'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the version number to the packet.
        intermediate = self.struct.pack('>B', self._header.get('version'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the yoho value to the packet.
        intermediate = self.string_packer(self._header.get('yoho'))
        for byte in intermediate : raw_packet.append(byte)
        #Add the status word to the packet.
        intermediate = self._status.get('sensor_status')
        for byte in intermediate : raw_packet.append(byte)
        #Add the cog data to the packet.
        intermediate = self._cog_data.get('cog_data')
        raw_packet.extend(intermediate)
        #Return the generated packet.
        return raw_packet

    #This function will generate a specified number of random gator packets.
    def generate_packets(self, num_packets):
        #Create byte array of raw simulated data.
        raw_packets = bytearray()
        #Generate the specified number of packets.
        for _ in range(num_packets):
            raw_packets.extend(self.generate_packet())
        #Return the generated packets.
        return raw_packets

    