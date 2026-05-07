TITLE: Appointment
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Appointment.png
---

# Start
> at first i did an nmap scan that result of this
`
i used this to not waste time on all port so this challenge this about sql injection
 
labs nmap -min-rate 5000 T4 -Pn -p 0-9999 10.129.140.244 -o nmap_scan -v  
Warning: The -o option is deprecated. Please use -oN
Starting Nmap 7.99 ( https://nmap.org ) at 2026-05-07 17:43 +0000
Initiating Parallel DNS resolution of 1 host. at 17:43
Completed Parallel DNS resolution of 1 host. at 17:43, 0.50s elapsed
Initiating System DNS resolution of 1 host. at 17:43
Completed System DNS resolution of 1 host. at 17:43, 0.00s elapsed
Failed to resolve "T4".
Initiating Parallel DNS resolution of 1 host. at 17:43
Completed Parallel DNS resolution of 1 host. at 17:43, 0.50s elapsed
Initiating SYN Stealth Scan at 17:43
Scanning 10.129.140.244 [10000 ports]
Discovered open port 80/tcp on 10.129.140.244
Completed SYN Stealth Scan at 17:43, 2.08s elapsed (10000 total ports)
Nmap scan report for 10.129.140.244
Host is up (0.059s latency).
Not shown: 9999 closed tcp ports (reset)
PORT   STATE SERVICE
80/tcp open  http

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 3.17 seconds
           Raw packets sent: 10036 (441.584KB) | Rcvd: 10000 (400.004KB)


`
> after this i used browser to get the content use sql injection to bypass the login page

## Tasks



1. What does the acronym SQL stand for?
`
Structured Query Language
`

2. What is one of the most common type of SQL vulnerabilities?
`
SQL injection
`

3. What is the 2021 OWASP Top 10 classification for this vulnerability?
`
A03:2021-Injection
`

4. What does Nmap report as the service and version that are running on port 80 of the target?
`
Apache httpd 2.4.38 ((Debian))
`

5. What is the standard port used for the HTTPS protocol?
`
443
`

6. What is a folder called in web-application terminology?
`
directory
`

7. What is the HTTP response code that is returned for Not Found errors?
`
404
`

8. Gobuster is one tool used to brute force directories on a webserver. What switch do we use with Gobuster to specify we're looking to discover directories, and not subdomains?
`
dir
`

9. What single character can be used to comment out the rest of a line in MySQL?
`
#
`

10. If user input is not handled carefully, it could be interpreted as a comment. Use a comment to login as admin without knowing the password. What is the first word on the webpage returned?
> to get the flag u will ne to se sql injection admin'#

`
Congratulations
`

11. flag
`
e3d0796d002a446sc0e622226f42e9672

`
