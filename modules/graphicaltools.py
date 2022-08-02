""""
Written by Caleb C. & Andrew Valentini in 2022 for Carthage Space Sciences | WSGC | NASA
Graphs the strain data as an FFT plot
"""
import matplotlib.pyplot as plt
import numpy as np
from fosmodule import gatorpacket
class fftplot:        
    def produceplot(self, x, y):
        """"
        thispacket = gatorpacket()
        pkt_header, pkt_status, pkt_cog = thispacket.create_inner()
        pkt_timestamp = pkt_header.get_timestamp()
        strain_data = pkt_cog.get_strain_data()
        
        plt.figure(figsize=(10,10))
        plt.plot(pkt_timestamp, strain_data)
        plt.ylabel('Strain Data')
        plt.xlabel('Time (microseconds)')
        plt.show()
        """
        fig = plt.figure(figsize=(10,10))
        plt.plot(x,y)
        return fig