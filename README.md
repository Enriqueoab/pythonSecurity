# Repository of all related with the python-security hacking course

## Python & Ethical Hacking From Scratch

Common methods use to check object and variables, we are usig scapy as example:

- Display the fields that belong to the object:
```python
    print(arp_request.show())
```
Exaple response:

![show() method response example](https://github.com/Enriqueoab/pythonSecurity/blob/main/img/show%20method%20example.png)
- Print a concise summary of the packet's contents print a concise summary of the packet's contents:
```python
    print(arp_request.summary())
```
Exaple response:

![summary() method response example](https://github.com/Enriqueoab/pythonSecurity/blob/main/img/summary%20method%20example.png)

- To display the names of the fields of a class:
```python
    scapy.ls(scapy.ARP())
```
Exaple response:

![ARP() method response example](https://github.com/Enriqueoab/pythonSecurity/blob/main/img/ls%20method%20example.png)

### Command to run the network_scanner script:

 **/24 Allowed to go through all the range from 0 to 254**
```sh
python  network_scanner.py --target {OUR_IP}/24
```

## ARP spoofing hacking

### Concepts related to the project.

 - ARP (Address Resolution Protocol): Is in charge of help in finding the MAC address of a device within a local network.

 - MAC: Unique hardware addresses assigned to network interface cards. It is used for actual data transmission at the hardware level

 - Network Interface Card (NIC): Sometimes referred to as a network adapter or network card, is a hardware component that connects
   a computer or other device to a network. Its primary function is to provide the physical interface between the device and the network,
   enabling communication between the device and other devices or servers on the same network or the broader internet.

 - IP: addresses are used for routing data across the broader internet.

 - ARP table: It is also known as an ARP cache, is a table maintained by network devices, such as computers and routers, to store a mapping between IP addresses
   and corresponding MAC addresses within a local network.

 ### How ARP works?

 ## How [ARP](#arp) Works

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


## How [ARP](#arp) spoofing Works:

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

# [Arp spoof](ADD URL TO THE SCRIPT) script:

##Objective:
- Redirect the flow of other packets, of other devices, through our computer.

##Steps:

1. **We are going to create an arp packet. To set, in the victim records, the router MAC address as ours**

- op=2 -> Use to send the ARP as a respond not a request, which would be 1.
- pdst="10.0.2.7" -> Destination IP, which is the one of the target device.
- hwdst="08:00:27:08:af:07" -> Hardware destination, MAC address of the target device.
- psrc="10.0.2.1" -> Source IP, that is set as the IP of the router to associate it, in the [ARP table](#arp_table) of the victim, with the MAC address
  of the attacker device.

```python
    scapy.ARP(op=2, pdst="10.0.2.7", hwdst="08:00:27:08:af:07", psrc="10.0.2.1")
```

2. **Sending the packet**

```python
    scapy.send(arp_packet)
```

3. ****