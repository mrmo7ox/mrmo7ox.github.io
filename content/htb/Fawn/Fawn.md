TITLE: Fawn
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/fawn.png
---

# Start:

*i started by using nmap scan:*

`
# Nmap 7.99 scan initiated Thu May  7 13:00:43 2026 as: /usr/lib/nmap/nmap -sV -o nmap_scan 10.129.140.122
Nmap scan report for 10.129.140.122
Host is up (0.88s latency).
Not shown: 824 closed tcp ports (reset), 175 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu May  7 13:00:50 2026 -- 1 IP address (1 host up) scanned in 7.03 seconds
`

## Tasks

1. What does the 3-letter acronym FTP stand for?
`
File Transfer Protocol
`
2. Which port does the FTP service listen on usually?
`
21
`
3. FTP sends data in the clear, without any encryption. What acronym is used for a later protocol designed to provide similar functionality to FTP but securely, as an extension of the SSH protocol?
`
SFTP
`
4. What is the command we can use to send an ICMP echo request to test our connection to the target?
`
ping
`
5. From your scans, what version is FTP running on the target?
`
vsftpd 3.0.3
`
6. From your scans, what OS type is running on the target?
`
Unix
`
7. What is the command we need to run in order to display the 'ftp' client help menu?

`
ftp -?
`
8. What is username that is used over FTP when you want to log in without having an account?
`
anonymous
`
9. What is the response code we get for the FTP message 'Login successful'?
`
230
`
10. There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system.
`
ls
`
11. What is the command used to download the file we found on the FTP server?
`
get
`
12. Submit root flag

> to get the flag u need to connect using the ftp command 
```bash
-> ftp anonymous@<ip> -P 21
# use empty password

->get flag.txt
->exit 
->cat flag.txt

```




