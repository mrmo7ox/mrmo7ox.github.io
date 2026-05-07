TITLE: Meow
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/meow.png
---
# Start:
*this is my first time try this so im going to talk about how i connect to the server*
1. i has to create a docker container of kalilinux/kali-rolling with openvpn
2. donwloaded the openvpn config file to  connect to the vlan of the server using 
tmux to split the screen
```
Hack The Box (HTB) uses OpenVPN to create a secure, direct network link between your local machin.
(usually a Virtual Machine) and their private, isolated labs. By using an OpenVPN configuration file, your machine is assigned an IP address within the HTB subnet, allowing you to scan, attack, and interact with the target machines as if they were on your own local network.

```
3. i used `nmap -sV <ip>` to indentify the open ports
`
# Nmap 7.99 scan initiated Thu May  7 10:28:54 2026 as: /usr/lib/nmap/nmap -sV -o nmap_scan 10.129.117.160
Nmap scan report for 10.129.117.160
Host is up (0.062s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
23/tcp open  telnet  Linux telnetd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu May  7 10:29:08 2026 -- 1 IP address (1 host up) scanned in 13.36 seconds
`
> as u can see there is a open 23 port that serve telnet server

### now the Tasks

1. What does the acronym VM stand for?
`
virtual machine
`
2. What tool do we use to interact with the operating system in order to issue commands via the command line, such as the one to start our VPN connection? It's also known as a console or shell.

`
terminal
`
3. What service do we use to form our VPN connection into HTB labs?
`
openvpn

`
4. What tool do we use to test our connection to the target with an ICMP echo request?
`
ping
`
5. What is the name of the most common tool for finding open ports on a target?

`
nmap
`
6. What service do we identify on port 23/tcp during our scans?
`
telnet
`
7. What username is able to log into the target over telnet with a blank password?
`
root
`
8. flag (install telnet and connect using the root as username and empty pass) 
> cat ./flag
`
b40abdfe23665f766f9c61ecba8a4c19
`
