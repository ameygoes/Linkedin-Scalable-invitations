from cryptography.fernet import Fernet
import os

from Configs.envrinomentSpecificConfgis import CREDS_FILE
from Configs.jobConfigs import ENCRYPTED_EMAIL

def generate_key():
    if os.path.exists(CREDS_FILE):
        print(f"The file '{CREDS_FILE}' exists in the folder.")
    else:
        key = Fernet.generate_key()
        with open(CREDS_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "rb") as key_file:
            key = key_file.read()
        return key
    else:
        generate_key()
        return load_key()


def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode('utf-8'))
    return decrypted_message.decode('utf-8')

def get_email():
    key = load_key()
    encrypted_email = decrypt_message(ENCRYPTED_EMAIL, key)
    return encrypted_email