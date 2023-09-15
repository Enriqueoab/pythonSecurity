#!/usr/bin/env python
import netfilterqueue # I didn't install it
import scapy.all as scapy
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # Converting it as scapy packet, that way we will able to handle it in a simpler way
    print(scapy_packet.show()) # packet.get_payload() would show, properly, just the "raw" layer
    # packet.accept() # To forward the packet to the destination
    packet.drop() # To cut the internet connection of the client

queue = netfilterqueue.NetfilterQueue() #creating an instance of a net filter queue object
        #(--queue-num value set before, call back function for each vaue in the queue)
queue.bind(0, process_packet) #  This method allows us to do is to connect or bind this Q to the Q that we created previusly (In the terminal)
queue.run()