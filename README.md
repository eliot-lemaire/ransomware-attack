Tutorial
Recommended Setup:

To test this, I recommend using 2 EC2 instances.
VICTIM (Target Machine Setup)

On the victim machine, you'll need to install Cryptography and Tor. You can use the following script to automate the setup:

sudo apt update
sudo apt install python3-pip
pip install cryptography
sudo apt install tor

Once that's done, you will need to run ransomware.py on the victim's machine.
RECEIVER (Attacker's Machine Setup)

On the attacker machine, run the following commands to install the necessary tools:

sudo apt update
sudo apt install python3-pip
sudo apt install tor

Then, configure Tor to run a hidden service:

sudo nano /etc/tor/torrc

In the torrc file, add the following lines:

HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 12345 127.0.0.1:12345

Restart Tor:

sudo systemctl restart tor

To find the .onion address, run:

sudo cat /var/lib/tor/hidden_service/hostname

Copy the .onion address that is displayed and update it in ransomware.py on the victim’s machine.
Execution Steps
Step 1:

    On the attacker's machine, run the listener.py script.

    On the victim's machine, run the ransomware.py script.

Step 2:

    The attacker will receive a key to decrypt the file.

    On the victim's machine, run the decrypt.py script, and edit the key.key file using:

nano key.key

Paste the decryption key into the file.

Enjoy!
