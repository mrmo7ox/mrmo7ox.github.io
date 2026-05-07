TITLE: Crocodile
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Crocodile.png
---

# Start
> at first i did an nmap scan that result of this
`

`
**N.B**
after the nmap scan i use the browser to find the email
now i need something to find the subdomain but we have a problem we have ip
not a domain 
so u will need to add domain name thetoppers.htb to /etc/hosts
like this 
```bash
vim /etc/hosts

#add this line 

10.129.141.104 thetoppers.htb
```
## Tasks
1. What Nmap scanning switch employs the use of default scripts during a scan?
`
-sC
`

2. What service version is found to be running on port 21?
`
vsftpd 3.0.3
`

3. What FTP code is returned to us for the "Anonymous FTP login allowed" message?
`
230
`

4. After connecting to the FTP server using the ftp client, what username do we provide when prompted to log in anonymously?
`
anonymous
`

5. After connecting to the FTP server anonymously, what command can we use to download the files we find on the FTP server?
`
get
`

6. What is one of the higher-privilege sounding usernames in 'allowed.userlist' that we download from the FTP server?
`
admin
`

7. What version of Apache HTTP Server is running on the target host?
`
Apache httpd 2.4.41
`

8. What switch can we use with Gobuster to specify we are looking for specific filetypes?
`
-x
`

9. Which PHP file can we identify with directory brute force that will provide the opportunity to authenticate to the web service?
`
login.php
`

10. Submit root flag

0. used gobuster to find the login page they hinted on the question
`
gobuster dir -u 10.129.141.51  -w /usr/share/seclists/Discovery/Web-Content/raft-small-files.txt
`

1. i used the anonymous login with theftp server to login and get the list of usernames and passwords
 
2. to get the flag u will need to use hydra to brute force the login page

`
hydra -L ./allowed.userlist -P ./allowed.userlist.passwd 10.129.141.51 http-post-form "/login.php:Username=^USER^&Password=^PASS^&Submit=Login:F=Warning! Incorrect information."
`
3. after this get the correct username and password find the flag in the /index.php
`
c7110277ac44d78b6a9fff2232434d16
`


