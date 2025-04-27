from cryptography.fernet import Fernet
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

    # Load the key from the 'key.key' file
    try:
        with open("key.key", "rb") as thekey:
            key = thekey.read()
    except Exception as e:
        print(f"Failed to load key: {e}")
        exit(1)

    fernet = Fernet(key)

    for file in files:
        filename = os.path.basename(file)
        if filename in ("decrypte.py", "ransomware.py", "key.key"):
            continue
        try:
            # Read the encrypted contents of the file
            with open(file, "rb") as thefile:
                contents = thefile.read()

            # Decrypt the contents
            contents_decrypted = fernet.decrypt(contents)

            # Overwrite the file with the decrypted contents
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)

            print(f"Decrypted {file}")
        except Exception as e:
            print(f"Failed to decrypt {file}: {e}")
