#!/usr/bin/python3

from mythic import mythic
from utils.auth import *
import secrets, string

# Generates a password with the secrets module
def generate_password():
    valid_chars = string.ascii_letters + string.digits
    password = "".join(secrets.choice(valid_chars) for i in range(16))
    return password

# Creates a new operator account and returns the credentials to dump to disk later
async def create_user(mythic_instance: mythic, username: str):
    password = generate_password()
    results = await mythic.create_operator(mythic=mythic_instance, username=username, password=password)
    credentials = username + ":" + password
    print(results)
    print("Creds: " + credentials)
    return credentials