from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64
import os
import getpass 

from pathlib import Path

# Determine location of secrets
# If true, create secrets dir in same location as this script. Else, make it in the home directory.
LOCAL_SECRET = True 
if LOCAL_SECRET:
    secret_dir = Path('.secrets')
else:
    secret_dir = Path.home()/'.secrets'
secret_dir.mkdir(exist_ok=True)

# Initialise project directories
while True:
    project_name = input('Enter a name for the wallet/project: ')
    project_dir = secret_dir/project_name
    try: 
        project_dir.mkdir()
        print(f'Created project directory at {project_dir}!')
        break
    except: 
        print('Project already exists, pick a new one!')

# Ask for password and convert to bytes
while True:
    password = getpass.getpass('Enter password: ')
    password2 = getpass.getpass('Enter password again: ')
    if password==password2:
        password = bytes(password, 'ascii')
        break
    else:
        print("These don't match, fool")

# Ask for seedphrase, this is the item to be encrypted
seedphrase = input('Enter Seed Phrase: ')

# Create and store salt
salt = os.urandom(16)
f = open(project_dir/'salt.txt', 'wb')
f.write(salt)
f.close()

# Derive key and use it to encrypt the phrase
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Create fernet encrypting object
fern = Fernet(key)
token = fern.encrypt(bytes(seedphrase,'ascii'))

f = open(project_dir/'encrypted.txt','wb')
f.write(token)
f.close()

print('Done!')

