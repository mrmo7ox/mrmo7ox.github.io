TITLE: Dancing
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/dancing.png
---

# Start
> at first i did an nmap scan that result of this
`
# Nmap 7.99 scan initiated Thu May  7 13:37:21 2026 as: /usr/lib/nmap/nmap -sV -p 445 -o nmap_scan 10.129.140.150
Nmap scan report for 10.129.140.150
Host is up (0.057s latency).

PORT    STATE SERVICE       VERSION
445/tcp open  microsoft-ds?

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu May  7 13:37:48 2026 -- 1 IP address (1 host up) scanned in 27.05 seconds

`
> so after this i did start search about it what is SMB
* so smb stants for server message block that is used by windows so share files*
* its used by printers, and network ports*

## Tasks

1. What does the 3-letter acronym SMB stand for?
`
Server Message Block
`

2. What port does SMB use to operate at?
`
445
`

3. What is the service name for port 445 that came up in our Nmap scan?
`
microsoft-ds
`

4. What is the 'flag' or 'switch' that we can use with the smbclient utility to 'list' the available SMB shares on Dancing?
`
-L
`

5. How many shares are there on Dancing?
`
4
`

6. What is the name of the share we are able to access in the end with a blank password?
`
WorkShares
`

7. What is the command we can use within the SMB shell to download the files we find?
`
get
`

8. Submit root flag
`
5f61c10dffbc77a704d76016a22f1664
`
