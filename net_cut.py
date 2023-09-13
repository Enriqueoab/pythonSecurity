#!/usr/bin/env python
import netfilterqueue # I didn't install it

def process_packet(packet):
    print(packet)
    packet.accept()
    packet.drop()

queue = netfilterqueue.NetfilterQueue() #creating an instance of a net filter queue object
        #(--queue-num value set before, call back function for each vaue in the queue)
queue.bind(0, process_packet) #  This method allows us to do is to connect or bind this Q to the Q that we created previusly (In the terminal)
queue.run()