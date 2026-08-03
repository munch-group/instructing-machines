import base64
import os, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--decrypt', action='store_true',
                help='Decrypt input file.')
parser.add_argument('--overwrite', action='store_true',
                help='Overwrite existing files.')
parser.add_argument('encryptionkey', type=str,
                help='Passkey for encryption.')
parser.add_argument('inputfile', type=Path, help='Input file name')

args = parser.parse_args()

encryptionkey_provided = args.encryptionkey
encryptionkey = encryptionkey_provided.encode() # Convert to type bytes
salt = b'he\xfdT(LL\xbc6V\xa8T\xf3\x1b\xf7\x13' # from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(encryptionkey)) # Can only use kdf once

def decrypt(input_file, output_file):

    print(f"Decrypting {input_file}")

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    try:
        encrypted = fernet.decrypt(data)
    except InvalidToken:
        print("Wrong encryption key")
        sys.exit()

    with open(output_file, 'wb') as f:
        f.write(encrypted)

def encrypt(input_file, output_file):

    print(f"Encrypting {input_file}")

    output_file = input_file.with_suffix(input_file.suffix + '.encrypted')
    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

if args.inputfile.is_dir():
    input_files = [p for p in args.inputfile.rglob("*") if p.is_file()]
else:
    input_files = [args.inputfile]


if args.decrypt:
    output_files = [p.with_suffix('') for p in input_files]
else:
    output_files = [p.with_suffix('.encrypted') for p in input_files]

if any(p.exists() for p in output_files) and not args.overwrite:
    print("Output files exists. Use --overwrite to overwrite existing files.")
    sys.exit()

if args.decrypt:
    for input_file, output_file in zip(input_files, output_files):
        if input_file.suffix == '.encrypted':
            decrypt(input_file, output_file)
else:
    for input_file, output_file in zip(input_files, output_files):
        if input_file.suffix != '.encrypted':
            encrypt(input_file, output_file)
