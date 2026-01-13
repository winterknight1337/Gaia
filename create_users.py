#!/usr/bin/python3

from mythic import mythic
import asyncio, sys, secrets, string

# Modify these parameters until I develop a real CLI
login_username = "mythic_admin"
login_password = "" # Add password
login_server_ip = "" # Add server IP address
login_server_port = 7443

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


def main():
    # Read the usernames for the accounts that are to be created
    with open("users.txt", "r") as users:
        user_list = users.readlines()
    
    # Authenticate to Mythic
    mythic_session = asyncio.run(login(username=login_username, password=login_password, server_ip=login_server_ip, server_port=login_server_port))
    print(mythic_session)

    # Create a user account
    for i in user_list:
        # Strips the trailing newline which prevented successful user logins and enables password dump to work correctly
        i = i.strip()

        # Actually creates the user
        created_user = asyncio.run(create_operator(mythic_instance=mythic_session, username=i))

        # Dump creds to file
        with open("creds.txt", "a") as creds:
            creds.write(created_user + "\n")

main()
sys.exit()