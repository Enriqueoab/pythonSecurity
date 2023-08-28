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
