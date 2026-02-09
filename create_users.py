#!/usr/bin/python3

from mythic import mythic
from dotenv import load_dotenv
import asyncio, os, sys, secrets, string

# Load the environmnet file .env
load_dotenv()

# Mythic login creds
login_username = os.getenv("MYTHIC_LOGIN_USERNAME")
login_password = os.getenv("MYTHIC_LOGIN_PASSWORD")
login_server_ip = os.getenv("MYTHIC_LOGIN_SERVER_HOST")
login_server_port = os.getenv("MYTHIC_LOGIN_SERVER_PORT")

# logs into mythic to begin user creation
async def login(username: str, password: str, server_ip: str, server_port: int):
    mythic_instance = await mythic.login(
        username=username,
        password=password,
        server_ip=server_ip,
        server_port=server_port,
        timeout=-1
    )
    return mythic_instance


# Generates a password with the secrets module
def generate_password():
    valid_chars = string.ascii_letters + string.digits
    password = "".join(secrets.choice(valid_chars) for i in range(16))
    print(password)
    return password


# Creates a new operator account and returns the credentials to dump to disk later
async def create_operator(mythic_instance: mythic, username: str):
    password = generate_password()
    results = await mythic.create_operator(mythic=mythic_instance, username=username, password=password)
    credentials = username + ":" + password
    print(results)
    print("Creds: " + credentials)
    return credentials

async def main():
    # Read the usernames for the accounts that are to be created
    with open("users.txt", "r") as users:
        user_list = users.readlines()
    
    # Authenticate to Mythic
    mythic_session = await login(username=login_username, password=login_password, server_ip=login_server_ip, server_port=login_server_port)
    print(mythic_session)

    # Create a user account
    for i in user_list:
        # Strips the trailing newline which prevented successful user logins and enables password dump to work correctly
        i = i.strip()

        # Actually creates the user
        created_user = await create_operator(mythic_instance=mythic_session, username=i)

        # Dump creds to file
        with open("creds.txt", "a") as creds:
            creds.write(created_user + "\n")

main()
sys.exit()