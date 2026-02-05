#!/usr/bin./python3

from mythic import mythic
from dotenv import load_dotenv
import asyncio, os, sys

# Load the environment file .env
load_dotenv()

# Mythic login creds
login_username = os.getenv("MYTHIC_LOGIN_USERNAME")
login_password = os.getenv("MYTHIC_LOGIN_PASSWORD")
login_server_ip = os.getenv("MYTHIC_LOGIN_SERVER_HOST")
login_server_port = os.getenv("MYTHIC_LOGIN_SERVER_PORT")

operation_name = os.getenv("MYTHIC_OPERATION_NAME")

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

async def create_operation(mythic_instance: mythic, operation_name: str):
    results = await mythic.create_operation(mythic=mythic_instance, operation_name=operation_name)
    print(results)
    return results

async def add_operator_to_operation(mythic_instance: mythic, operation_name: str, username: str):
    results = await mythic.add_operator_to_operation(mythic=mythic_instance, operation_name=operation_name, operator_username=username)
    print(results)
    return results

def main():
    # Read the usernames for the accounts that are to be assigned to the new operation
    with open("users.txt", "r") as users:
        user_list = users.readlines()

    # Authenticate to Mythic
    mythic_session = asyncio.run(login(username=login_username, password=login_password, server_ip=login_server_ip, server_port=login_server_port))
    print(mythic_session)

    # Creates a new operation
    asyncio.run(create_operation(mythic_session, operation_name))

    for i in user_list:
        # Strips whitespaces and newlines
        i = i.strip()

        # Assigns the operator to the new operation
        asyncio.run(add_operator_to_operation(mythic_session, operation_name, i))
