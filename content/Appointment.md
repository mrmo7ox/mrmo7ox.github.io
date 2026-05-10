TITLE: Appointment
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Appointment.png
---

# Appointment

Appointment is a simple laboratory that demonstrates a basic SQL Injection (SQLi) vulnerability on a login form.

## Recon

The initial scan shows only the web server is open.

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 80 | HTTP | Apache httpd 2.4.38 ((Debian)) |

## Exploitation

The website features a login portal. Since we don't have credentials, we test for SQL injection in the username field.

1. **Payload**: `' OR 1=1-- -`
2. **Result**: The query becomes `SELECT * FROM users WHERE username = '' OR 1=1-- -' AND password = '...'`. Since `1=1` is always true, the database returns the first user record (usually the admin), logging us in.

Once logged in, the flag is displayed on the dashboard.

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What does the acronym SQL stand for? | `Structured Query Language` |
| 2 | What is one of the most common type of vulnerabilities in web applications that allows an attacker to interfere with the queries that an application makes to its database? | `SQL Injection` |
| 3 | What does PII stand for? | `Personally Identifiable Information` |
| 4 | What is the 2021 OWASP Top 10 classification that SQL injection falls under? | `A03:2021-Injection` |
| 5 | What is the port number for HTTP? | `80` |
| 6 | What is the port number for HTTPS? | `443` |
| 7 | What is the name of the web server software used on the target? | `Apache` |
| 8 | What is the version of the web server software? | `2.4.38` |
| 9 | Submit root flag | `e3d0f53c94411fb162489c676d91f24d` |
