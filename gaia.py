import argparse, sys, os, asyncio, dotenv, shutil

# Load environment variables first
if os.path.isfile(".env"):
    config = dotenv.dotenv_values(".env")

#################################################################### CLI PARSING ####################################################################

# Root options that are available across the whole application
global_parser = argparse.ArgumentParser(
    prog='gaia.py',
    description='Lightweight helper tool to deploy and manage mythic c2 installs.')

# 'Core' modules
subparsers = global_parser.add_subparsers(title='modules', help='', dest='subcommand')
auth_parser = subparsers.add_parser('auth', help='authenticate to mythic and dump api key to .env')
# c2_profile_parser = subparsers.add_parser('c2-profiles', help='manage mythic c2 profiles')
# dns_parser = subparsers.add_parser('dns', help='manage dns records')
# install_parser = subparsers.add_parser('install', help='manage mythic installation')
operation_parser = subparsers.add_parser('operation', help='manage mythic operations')
# payload_parser = subparsers.add_parser('payloads', help='manage payloads')
user_parser = subparsers.add_parser('users', help='manage mythic users')

# Global modules
global_parser.add_argument('-k', '--no-ssl', action='store_true', help='disable ssl verification checks')

# Auth modules
auth_parser.add_argument('-s', '--mythic-server', required=True, nargs=1, metavar='', help="fqdn or ip address for mythic server")
auth_parser.add_argument('-p', '--mythic-port', required=True, nargs=1, metavar='', help="port for admin interface on mythic server. Defaults to 7443.")
auth_parser.add_argument('-aP', '--auth-password', required=True, nargs=1, metavar='', help='password for mythic user account')
auth_parser.add_argument('-aU', '--auth-user', required=True, nargs=1, metavar='', help='mythic user account to authenticate as')

# User modules
action_user_parser = user_parser.add_mutually_exclusive_group(required=True)
action_user_parser.add_argument('-c', '--create', action='store_true', help='creates user accounts in mythic')
# action_user_parser.add_argument('-d', '--delete', action='store_true', help='deletes user accounts in mythic') 
user_parser.add_argument('-u', '--users', nargs='+', metavar='', help='provide one or more user account to process')

# TODO implement the rest of these after getting basic POC out
# user_parser.add_argument('-oF', '--output-file', metavar='path/to/output', help='dumps newly created credentials to disk')
# user_parser.add_argument('-oS', '--output-stdout', metavar='', help='sends newly created creds to stdout')
# user_parser.add_argument('-uL', '--user-list', nargs='?', metavar="path/to/user_list", help='provide a path to a list of users')

# Operation Administration
operation_parser.add_argument('-o', '--operation', required=True, nargs=1, metavar='', help='specify operation to manage')
operation_parser.add_argument('-c', '--create', action='store_true', help='creates operations in mythic')
operation_parser.add_argument('-u', '--users', nargs='+', metavar='', help='provide user accounts to process')

action_operation_parser = operation_parser.add_mutually_exclusive_group()
action_operation_parser.add_argument('-a', '--assign', action='store_true', help='assigns users to an operations')
action_operation_parser.add_argument('-r', '--remove', action='store_true', help='removes users from an operations')


args = global_parser.parse_args()

##################################################################  END CLI PARSING ##################################################################


async def main():
    import utils.auth
    if args.subcommand == "auth":
        import utils.env
        
        # Authenticates to mythic if server, port, user, and password are specified
        auth_user = str(args.auth_user[0]).strip()
        auth_password = str(args.auth_password[0]).strip()
        mythic_host = str(args.mythic_server[0]).strip()
        mythic_port = int(args.mythic_port[0])

        # Auth according to SSL input
        if args.no_ssl == False:
            mythic_session = await utils.auth.mythic_login_with_user_creds(username=auth_user, password=auth_password, server_host=mythic_host, server_port=mythic_port)
        elif args.no_ssl == True:
            mythic_session = await utils.auth.mythic_login_with_user_creds_no_ssl(username=auth_user, password=auth_password, server_host=mythic_host, server_port=mythic_port)
        else:
            print("Unknown error in SSL processing during mythic authentication flow. Exiting!")
            sys.exit(1)

        # Create an API key for the current user
        api_token = await utils.auth.mythic_get_api_token(mythic_instance=mythic_session)    

        # Dumps API key and mythic connection information into .env
        # Copies .env-template to .env before population if .env does not currently exist
        if os.path.isfile(".env-template") == True and os.path.isfile(".env") == False:
            shutil.copy(".env-template", ".env")
            with open(".env", "r") as file:
                data = file.readlines()
        
        # Loads .env to prep for population
        elif config != None:
            with open(".env", "r") as file:
                data = file.readlines()

        # Populates updated values for .env
        for i in range(len(data)):
            if "MYTHIC_LOGIN_SERVER_HOST" in data[i]:
                data[i] = utils.env.populate_dotenv_var_string(data[i], mythic_host)

            elif "MYTHIC_LOGIN_SERVER_PORT" in data[i]:
                data[i] = utils.env.populate_dotenv_var_int(data[i], mythic_port)

            elif "MYTHIC_API_KEY" in data[i]:
                data[i] = utils.env.populate_dotenv_var_string(data[i], api_token)

            else:
                pass

        with open(".env", "w") as file:
            file.writelines(data)
        sys.exit(0)
    
    # Authenticates to mythic with API key if auth is not specified
    api_key = config["MYTHIC_API_KEY"]
    mythic_host = config["MYTHIC_LOGIN_SERVER_HOST"]
    mythic_port = config["MYTHIC_LOGIN_SERVER_PORT"]
    mythic_session = await utils.auth.mythic_login_with_api(api_token=api_key, server_host=mythic_host, server_port=mythic_port)

    # Manages users
    if args.subcommand == "users":
        import utils.users, utils.operations

        # Get current operations to prepare to assign a default for a new user
        operations = await utils.operations.get_operations(mythic_instance=mythic_session)
        default_operation = operations[0]
        
        # Create new users before assigning them to default operation (The first opeation that returns when getting all operations)
        if args.create == True:
            users = args.users
            for i in users:
                await utils.users.create_user(mythic_instance=mythic_session, username=i)
                await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=default_operation["name"], username=i)

        sys.exit(0)

    # Process operations
    if args.subcommand == "operation":
        import utils.operations, utils.env

        # Creates new operation
        if args.create == True:
            operation = str(args.operation[0]).strip()
            await utils.operations.create_operation(mythic_instance=mythic_session, operation_name=operation)

            # Modify env to include new operation
            utils.env.modify_env("MYTHIC_OPERATION_NAME", operation, ".env-template", )

        # Assign users to operations
        if args.assign == True:
            operation = args.operation
            users = args.users
            for i in operation:
                for j in users:
                    await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=i, username=j)

        sys.exit(0)


if __name__ == '__main__':
     asyncio.run(main())
sys.exit(0)