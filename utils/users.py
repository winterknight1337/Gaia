from mythic import mythic
import secrets, string

# Generates a password with the secrets module
def generate_password():
    valid_chars = string.ascii_letters + string.digits
    password = "".join(secrets.choice(valid_chars) for i in range(16))
    return password

# Creates a new operator account and returns the credentials to dump to disk later
async def create_user(mythic_instance: mythic, username: str):
    password = generate_password()
    await mythic.create_operator(mythic=mythic_instance, username=username, password=password)
    credentials = username + ":" + password
    return credentials

def prepare_users(users_stdin: str, user_file_in: str):
    # Load user list from file, set list to empty if not passed
    if user_file_in != None:
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
