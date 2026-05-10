TITLE: Fawn
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Fawn

Fawn is an introductory machine focusing on File Transfer Protocol (FTP) enumeration and anonymous access.

## Recon

Nmap reveals port 21 is open, running `vsftpd 3.0.3`.

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 21 | FTP | vsftpd 3.0.3 |

## Exploitation

We can attempt to log in anonymously to the FTP server.

```bash
ftp 10.129.142.167
Name: anonymous
Password: 
```

Once logged in, we list the files:

```bash
ftp> ls
-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
ftp> get flag.txt
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What does the 3-letter acronym FTP stand for? | `File Transfer Protocol` |
| 2 | Which port does the FTP service listen on by default? | `21` |
| 3 | What is the 4-letter acronym for the FTP protocol which uses an encrypted connection? | `SFTP` |
| 4 | What is the command we can use to send an ICMP echo request to test our connection to the target? | `ping` |
| 5 | From your scans, what version is FTP running on the target? | `vsftpd 3.0.3` |
| 6 | From your scans, what OS type is running on the target? | `Unix` |
| 7 | What is the command we need to run in order to display the 'ftp' client help menu? | `ftp -h` |
| 8 | What is username that is used over FTP when you want to log in without having an account? | `anonymous` |
| 9 | What is the response code we get for the FTP message 'Login successful'? | `230` |
| 10 | There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system. | `ls` |
| 11 | What is the command used to download the file we found on the FTP server? | `get` |
| 12 | Submit root flag | `b40abdfe23665f766f9c61ecba8a4c19` |
