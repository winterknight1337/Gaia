from mythic import mythic

# logs into mythic with creds
async def mythic_login_with_user_creds(username: str, password: str, server_host: str, server_port: int):
    mythic_instance = await mythic.login(
        username=username,
        password=password,
        server_ip=server_host,
        server_port=server_port,
        timeout = -1
    )
    return mythic_instance

# logs into mythic with api token
async def mythic_login_with_api(api_token: str, server_host: str, server_port: int):
    mythic_instance = await mythic.login(
        apitoken=api_token,
        server_ip=server_host,
        server_port=server_port,
        timeout = -1
    )
    return mythic_instance

# logs into mythic with creds without ssl
async def mythic_login_with_user_creds_no_ssl(username: str, password: str, server_host: str, server_port: int):
    mythic_instance = await mythic.login(
        username=username,
        password=password,
        server_ip=server_host,
        server_port=server_port,
        timeout = -1,
        ssl=False
    )
    return mythic_instance

# logs into mythic with api token without ssl
async def mythic_login_with_api_no_ssl(api_token: str, server_host: str, server_port: int):
    mythic_instance = await mythic.login(
        apitoken=api_token,
        server_ip=server_host,
        server_port=server_port,
        timeout = -1,
        ssl=False
    )
    return mythic_instance

async def mythic_get_api_token(mythic_instance:mythic):
    api_token = await mythic.create_apitoken(mythic=mythic_instance)
    print("API token dumped to .env file")
    return api_token