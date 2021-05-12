A very quick and dirty alternative for storing seed phrases.
Essentially a barebones password manager of sorts.

# Disclaimer
This is not at all secure. Only slightly more secure than storing seed phrases in plaintext.
The purpose of this is just for better management for developers who have 100s of seed phrases when working on development wallets.

# Usage
## Encrypt
`python encrypt.py`
Just follow the instructions. I usually use the wallet address as the project name.
You can set the `LOCAL_SECRET` variable in the encrypt file to determine if you wanna store the .secrets folder under the code directory or your home directory.

## Decrypt
`python decrypt.py`
This will display the seed phrase in plaintext at the end.
