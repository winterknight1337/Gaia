import os
from mythic import mythic

def create_local_gaia_ssh_key(key_name: str, key_contents: str):
    # Dump the new keypair to disk at ~/.ssh/gaia.pem overwriting an existing pair. This should work across both windows and linux. 
    home_dir = os.path.expanduser("~")
    ssh_dir = f"{home_dir}/.ssh/"
    with open(f"{ssh_dir}/{key_name}.pem", "w") as file:
        file.write(key_contents)


def delete_local_gaia_ssh_key(key_name:str):
    home_dir = os.path.expanduser("~")
    ssh_dir = f"{home_dir}/.ssh/"
    ssh_file = f"{ssh_dir}/{key_name}.pem" 
    
    if os.path.exists(ssh_file):
        os.remove(ssh_file)
    else:
        print("SSH Keyfile already removed, skipping.")

async def generate_redirector_rules(mythic_instance: mythic, payload_uuid: str):
    redir_rules = await mythic.execute_custom_query(
        mythic=mythic_instance,
        query = """
        query generateRedirectRulesMutation($uuid: String!) {
            redirect_rules(uuid: $uuid) {
                status
                error
                output
                __typename
            }
        }
        """,
        variables={"uuid" : payload_uuid}
    )

    return redir_rules