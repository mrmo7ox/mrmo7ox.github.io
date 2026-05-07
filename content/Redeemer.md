TITLE: Redeemer
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Appointment.png
---

# Start:

*i started by using nmap scan:*
> nmap --min-rate 5000 -T4 -Pn -p 0-9999 10.129.140.184  -o nmap_scan -v
`
# Nmap 7.99 scan initiated Thu May  7 14:26:01 2026 as: /usr/lib/nmap/nmap --min-rate 5000 -T4 -Pn -p 0-9999 -o nmap_scan -v 10.129.140.184
Increasing send delay for 10.129.140.184 from 0 to 5 due to 11 out of 11 dropped probes since last increase.
Increasing send delay for 10.129.140.184 from 5 to 10 due to 190 out of 474 dropped probes since last increase.
Nmap scan report for 10.129.140.184
Host is up (0.073s latency).
Not shown: 9999 closed tcp ports (reset)
PORT     STATE SERVICE
6379/tcp open  redis

Read data files from: /usr/share/nmap
# Nmap done at Thu May  7 14:26:05 2026 -- 1 IP address (1 host up) scanned in 3.79 seconds

`
>nmap -A 10.129.140.184 -p 6379 -o nmap_scan
`
# Nmap 7.99 scan initiated Thu May  7 14:31:14 2026 as: /usr/lib/nmap/nmap -A -p 6379 -o nmap_scan 10.129.140.184
Nmap scan report for 10.129.140.184
Host is up (0.12s latency).

PORT     STATE    SERVICE VERSION
6379/tcp filtered redis
Too many fingerprints match this host to give specific OS details
Network Distance: 2 hops

TRACEROUTE (using proto 1/icmp)
HOP RTT       ADDRESS
1   146.54 ms 10.10.16.1
2   205.90 ms 10.129.140.184

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu May  7 14:31:24 2026 -- 1 IP address (1 host up) scanned in 10.17 seconds

` 
## Tasks

1. Which TCP port is open on the machine?
`
6379
`

2. Which service is running on the port that is open on the machine?
`
redis
`

3. What type of database is Redis? Choose from the following options: (i) In-memory Database, (ii) Traditional Database
`
In-memory Database
`

4. Which command-line utility is used to interact with the Redis server? Enter the program name you would enter into the terminal without any arguments.
`
redis-cli
`

5. Which flag is used with the Redis command-line utility to specify the hostname?
`
-h
`

6. Once connected to a Redis server, which command is used to obtain the information and statistics about the Redis server?
`
info
`

7. What is the version of the Redis server being used on the target machine?
`
to get the verison u should use info and find the version in the start of text

5.0.7
`

8. Which command is used to select the desired database in Redis?
`
select
`

9. How many keys are present inside the database with index 0?
`
4
`

10. Which command is used to obtain all the keys in a database?
`
keys *
`


11. Submit root flag
`

To get the flag  u should use 
select 0
KEYS *
GET flag

03e1d2b376c37ab3f5319922053953eb
`
