from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64
import os
import getpass 

from pathlib import Path

local_secret_dir = Path('.secrets')
home_secret_dir = Path.home()/'.secrets'

while True:
    project_name = input('Enter wallet name to be decrypted: ')
    project_dir = local_secret_dir/project_name

    if project_dir.is_dir(): 
        print(f'Located project directory at {project_dir}!')
        break

    elif (home_secret_dir/project_name).is_dir():
        project_dir = home_secret_dir/project_name
        print(f'Located project directory at {project_dir}!')
        break
    else:
        print('Wallet or project not found! Please try again.')


# Ask for password and convert to bytes
password = getpass.getpass('Enter Password to be used for decryption: ')
password = bytes(password, 'ascii')

# Create and store salt
f = open(project_dir/'salt.txt', 'rb')
salt = f.readline()
f.close()

# Derive key and use it to encrypt the phrase
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Read in encrypted seedphrase
f = open(project_dir/'encrypted.txt','rb')
token = f.readline()
f.close()

# Create fernet object
fern = Fernet(key)

# decrypt and print results
def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

yes_or_no('This will disply the seedphrase in plain text, are you sure?')
try: 
    fern.decrypt(token)
    print(fern.decrypt(token))
    print('Done!')
    
except:
    print('Invalid password!')