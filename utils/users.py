import secrets, string
from mythic import mythic
from prettytable import PrettyTable

# Generates a password with the secrets module
def generate_password():
    valid_chars = string.ascii_letters + string.digits
    password = "".join(secrets.choice(valid_chars) for i in range(16))
    return password

# Creates a new operator account and returns the credentials to dump to disk later
async def create_mythic_user(mythic_instance: mythic, username: str):
    password = generate_password()
    await mythic.create_operator(mythic=mythic_instance, username=username, password=password)
    credentials = username + ":" + password
    return credentials

def prepare_mythic_users(users_stdin: str, user_file_in: str):
    # Load user list from file, set list to empty if not passed
    if user_file_in != []:
        with open(user_file_in, 'r') as file:
            user_list = file.readlines()

        # Clean up newlines
        for i in range(len(user_list)):
            user_list[i] = user_list[i].strip()
    else:
        user_list = []

    # Avoid concatenation errors 
    if users_stdin == None:
        users_stdin = []

    # Merge and deduplicate user lists from file and stdin
    users = list(set(user_list + users_stdin))
    users.sort()
    
    return users

async def get_mythic_users(mythic_instance: mythic):
    users = await mythic.execute_custom_query(
        mythic=mythic_instance,
        query="""
            query getOperators {
            operator(order_by: {operation: {name: asc}}) {
                id
                username
                account_type
                active
                deleted
                admin
                last_failed_login_timestamp
                last_login
                operation {
                    id
                    name
                }
            }
        }
        """
        )
    return users

def print_mythic_users(mythic_users:dict):
    table = PrettyTable(["Username", "User ID", "Account Type", "Active", "Admin"])

    for i in mythic_users["operator"]:
        username = i["username"]
        user_id = i["id"]
        user_type = i["account_type"]
        user_active = i["active"]
        user_admin = i["admin"]

        table.add_row([username, user_id, user_type, user_active, user_admin])

    print(table)


# Still broken, need to figure out why. Works in Hasura console
async def delete_mythic_user(mythic_instance: mythic, user_id: int):
    user_del = await mythic.execute_custom_query(
        mythic=mythic_instance,
        query="""
            mutation delete_operator($id: Int!) {
            delete_operator(where: {id: {_eq: $id}}) {
                affected_rows
                }  
            }
        """,
        variables={"id" : user_id}
    )

    return user_del