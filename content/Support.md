TITLE: Support
CATEGORY: HackTheBox
DATE: 2026-05-11
IMAGE: ./assets/Support.png
---
# Support

Support is a machine that demonstrates Active Directory enumeration and reverse engineering of a .NET binary to recover LDAP credentials.

## Recon

### Nmap Scan

A full port scan reveals several open ports, including common Active Directory services like DNS (53), Kerberos (88), LDAP (389, 3268), and SMB (445).

```bash
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-05-11 13:29:06Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
```

### SMB Enumeration

Listing the SMB shares reveals a non-standard share named `support-tools`.

```bash
smbclient -L 10.129.230.181 -N
```

| Sharename | Type | Comment |
| :--- | :--- | :--- |
| ADMIN$ | Disk | Remote Admin |
| C$ | Disk | Default share |
| IPC$ | IPC | Remote IPC |
| NETLOGON | Disk | Logon server share |
| support-tools | Disk | support staff tools |
| SYSVOL | Disk | Logon server share |

We can connect to the `support-tools` share and find a ZIP file:

```bash
smbclient //10.129.230.181/support-tools -N
ftp> ls
# UserInfo.exe.zip
ftp> get UserInfo.exe.zip
```

## Exploitation

### Reverse Engineering UserInfo.exe

After unzipping the archive, we check the file type of `UserInfo.exe` using `diec`. It is a 32-bit PE file built with the .NET Framework.

```bash
diec UserInfo.exe
# PE32, Library: .NET Framework(v4.8, CLR v4.0.30319)
```

We can use `ilspycmd` or `ILSpy` (via Wine) to decompile the binary. Looking at the `LdapQuery` class and the `Protected` class, we find an encrypted password and a decryption routine.

#### Decompiled C# Code

```csharp
public LdapQuery()
{
    string password = Protected.getPassword();
    entry = new DirectoryEntry("LDAP://support.htb", "support\\ldap", password);
    // ...
}

internal class Protected
{
    private static string enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";
    private static byte[] key = Encoding.ASCII.GetBytes("armando");

    public static string getPassword()
    {
        byte[] array = Convert.FromBase64String(enc_password);
        byte[] array2 = array;
        for (int i = 0; i < array.Length; i++)
        {
            array2[i] = (byte)((uint)(array[i] ^ key[i % key.Length]) ^ 0xDFu);
        }
        return Encoding.Default.GetString(array2);
    }
}
```

### Decrypting the Credential

We can replicate the decryption logic in Python to recover the LDAP password:

```python
import base64

def get_password():
    enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
    key = b"armando"
    encrypted_bytes = base64.b64decode(enc_password)
    decrypted_chars = []
    
    for i in range(len(encrypted_bytes)):
        char_code = (encrypted_bytes[i] ^ key[i % len(key)]) ^ 0xDF
        decrypted_chars.append(chr(char_code))
    
    return "".join(decrypted_chars)

print(f"res: {get_password()}")
```

Running the script gives us the password:

- **LDAP Username:** `support\ldap`
- **LDAP Password:** `nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz`


