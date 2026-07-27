import argparse, sys, os, asyncio, dotenv, getpass, time, shutil

# Load environment variables first
if os.path.isfile(".env"):
    config = dotenv.dotenv_values(".env")
else:
    config = None

#################################################################### CLI PARSING ####################################################################

# Root options that are available across the whole application
formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=100, width=200)

global_parser = argparse.ArgumentParser(
    prog="gaia",
    description="Lightweight helper tool to install and manage Mythic c2 with a focus on students, CTF players, Mythic developers, and security researchers",
    formatter_class=formatter
    )

# Global switches
global_parser.add_argument('-v', "--version", action="version", version="%(prog)s v1.0", help="Display software version")


# Core modules
subparsers = global_parser.add_subparsers(title="Modules", dest="subcommand", help="")
install_parser = subparsers.add_parser(name="install", formatter_class=formatter, help="Installs Mythic on Debian, Ubuntu, or Kali")
auth_parser = subparsers.add_parser(name="auth", formatter_class=formatter, help="Authenticate to Mythic")
operation_parser = subparsers.add_parser(name="operation", formatter_class=formatter, help="Manage operations in Mythic")
user_parser = subparsers.add_parser(name="user", formatter_class=formatter, help="Manage users in Mythic")
payload_parser = subparsers.add_parser(name="payload", formatter_class=formatter, help="Manage payloads in Mythic")
dns_parser = subparsers.add_parser(name="dns", formatter_class=formatter, help="Manage DNS records with 3rd party registrars")
redir_parser = subparsers.add_parser(name="redirector", formatter_class=formatter, help="Manage redirector configuration within public clouds")


# Install options
install_parser.add_argument("--install-updates", action="store_true", help="Update target server with apt before installing Mythic")
install_parser.add_argument("--install-deps", action="store_true", help="Install dependencies required for Mythic on target server")
install_parser.add_argument("--install-mythic", action="store_true", help="Install Mythic on target server")
install_parser.add_argument("-S", "--server", required=True, type=str, metavar='', help="Hostname or IP address of target server")
install_parser.add_argument("-P", "--port", default=22, type=int, metavar='22', help="SSH port of target server")
install_parser.add_argument("-u", "--user", required=True, type=str, metavar='', help="User to authenticate as over SSH on target server")
install_parser.add_argument("-p", "--password", type=str, metavar='', help="SSH user password or SSH key passphrase")
install_parser.add_argument("-i", "--identity-file", type=str, metavar='path/to/file', help="SSH key for authentication")
install_parser.add_argument("--stderr", action="store_true", help="Show stderr from install steps from target server after stdout")


# Authentication options
auth_parser.add_argument("-S", "--server", required=True, type=str, metavar='', help="Hostname or IP address of Mythic server")
auth_parser.add_argument("-P", "--port", type=int, default=7443, metavar='7443', help="Port to access Mythic's web interface")
auth_parser.add_argument("-u", "--user", required=True, type=str, default="mythic_admin", metavar='mythic_admin', help="Target user for Mythic authentication")
auth_parser.add_argument("-p", "--password", required=True, action="store_true", help="Password for target user for Mythic authentication")
auth_parser.add_argument('-k', "--no-ssl", action="store_true", help="Don't verify TLS certificates when authenticating to Mythic")


# Mythic operations management
operation_subparser = operation_parser.add_subparsers(title="Operations", dest="operation", description="")
create_operation_subparser = operation_subparser.add_parser(name="create", formatter_class=formatter, help="Create new operations in Mythic")
create_operation_subparser.add_argument("-n", "--name", required=True, type=str, metavar='', help="Name of new operation in Mythic")

# delete_operation_subparser = operations_subparser.add_parser(name="delete", formatter_class=formatter, help="Delete existing operations in Mythic")
# delete_operation_subparser.add_argument("-n", "--name", required=True, type=str, metavar='', help="Specifies which operation to delete")

assign_operation_subparser = operation_subparser.add_parser(name="assign", formatter_class=formatter, help="Assign users to operations in Mythic")
assign_operation_subparser.add_argument("-o", "--operation-name", required=True, type=str, metavar='', help="Assign users to target operation")
assign_operation_subparser.add_argument("-u", "--users", required=True, nargs="+", type=str, metavar='', help="Users to be assigned to target operation")

operation_subparser.add_parser(name="list", formatter_class=formatter, help="List existing operations in Mythic")


# Mythic users management
user_subparser = user_parser.add_subparsers(title="User Actions", dest="user", description="")
create_user_subparser = user_subparser.add_parser(name="create", formatter_class=formatter, help="Create new users in Mythic")
create_user_subparser.add_argument("-u", "--users", nargs="+", type=str, metavar='', help="Specify usernames of new Mythic users")
create_user_subparser.add_argument("-l", "--user-list", type=str, metavar='path/to/file', help="Location of file listing users to be created")
create_user_subparser.add_argument("-d", "--cred-file", type=str, metavar='path/to/file', help="Location of file to dump newly created credentials")
create_user_subparser.add_argument("--cred-stdout", action="store_true", help="Print newly created user credentials to the terminal")

# delete_user_subparser = user_subparser.add_parser(name="delete", formatter_class=formatter, help="Delete users from Mythic")
# delete_user_subparser.add_argument("-u", "--users", required=True, nargs="+", type=list, metavar='', help="Specify usernames of Mythic users to delete")

# list_user_subparser = user_subparser.add_parser(name="list", formatter_class=formatter, help="Lists users in Mythic")

# assign_user_subparser = user_subparser.add_parser(name="assign", formatter_class=formatter, help="Assign users to operations in Mythic")
# assign_user_subparser.add_argument("-o", "--operation", required=True, type=str, metavar='', help="Assign users to target operation")
# assign_user_subparser.add_argument("-u", "--users", required=True, nargs="+", type=list, metavar='', help="Users to be assigned to target operation")


# Mythic payloads 
payload_subparser = payload_parser.add_subparsers(title="Payload Management", dest="payloads", description="")
create_payload_subparser = payload_subparser.add_parser(name="create", formatter_class=formatter, description="Create new payloads")

agent_subparser = create_payload_subparser.add_subparsers(title="Agents", dest="agent", help="Create a payload from the specified agent")
apollo_subparser = agent_subparser.add_parser(name="apollo", formatter_class=formatter, help="Manage Apollo payloads")
apollo_subparser.add_argument("-n", "--name", required=True, type=str, metavar='', help="Name of generated payload before file extensions")
apollo_subparser.add_argument("-u", "--callback-url", type=str, metavar='', help="URL (excluding port) the C2 agents will connect to")
apollo_subparser.add_argument("-p", "--callback-port", type=int, metavar='', default=80, help="Port that C2 agents will connect to (Default 80)")
apollo_subparser.add_argument("-k", "--callback-killdate", type=str, metavar='', help="Target date after which the C2 agents will no longer run (YYYY-MM-DD)")

poseidon_subparser = agent_subparser.add_parser(name="poseidon", formatter_class=formatter, help="Manage Poseidon payloads")
poseidon_subparser.add_argument("-n", "--name", required=True, type=str, metavar='', help="Name of generated payload before file extensions")
poseidon_subparser.add_argument("-u", "--callback-url", type=str, metavar='', help="URL (excluding port) the C2 agents will connect to")
poseidon_subparser.add_argument("-p", "--callback-port", type=int, metavar='', default=80, help="Port that C2 agents will connect to (Default 80)")
poseidon_subparser.add_argument("-k", "--callback-killdate", type=str, metavar='', help="Target date after which the C2 agents will no longer run (YYYY-MM-DD)")
poseidon_subparser.add_argument("-o", "--os", required=True, type=str, choices=["linux", "macos"], help="Build C2 agents for the target operating system")

athena_subparser = agent_subparser.add_parser(name="athena", formatter_class=formatter, help="Manage Athena payloads")
athena_subparser.add_argument("-n", "--name", required=True, type=str, metavar='', help="Name of generated payload before file extensions")
athena_subparser.add_argument("-u", "--callback-url", type=str, metavar='', help="URL (excluding port) the C2 agents will connect to")
athena_subparser.add_argument("-p", "--callback-port", type=int, metavar='', default=80, help="Port that C2 agents will connect to (Default 80)")
athena_subparser.add_argument("-k", "--callback-killdate", type=str, metavar='', help="Target date after which the C2 agents will no longer run (YYYY-MM-DD)")
athena_subparser.add_argument("-o", "--os", required=True, type=str, choices=["linux", "macos", "windows"], help="Build C2 agents for the target operating system")

# delete_payload_subparser = payload_subparser.add_parser(name="delete", formatter_class=formatter, description="Delete payloads")

list_payload_subparser = payload_subparser.add_parser(name="list", formatter_class=formatter, description="List current Mythic payloads")


# DNS management
# Cloudflare optionsc
dns_registrar_subparser = dns_parser.add_subparsers(title="Registrar", dest="registrar", description='')

cloudflare_subparser = dns_registrar_subparser.add_parser(name="cloudflare", formatter_class=formatter, help="Manage DNS records via Cloudflare")
cf_actions_subparser = cloudflare_subparser.add_subparsers(title="DNS Actions", dest="dns_action", description="Specify operation to perform")

# Creation actions
cf_create_subparser = cf_actions_subparser.add_parser(name="create", formatter_class=formatter, help="Create a new domain record")
cf_create_subparser.add_argument("-k", "--api-key", action="store_true", help="Enter Cloudflare API token when requested")
cf_create_subparser.add_argument("-d", "--domain", type=str, metavar='', help="Creates new records in target domain")
cf_create_subparser.add_argument("-n", "--record-name", type=str, metavar='', help="Name of new domain record")
cf_create_subparser.add_argument("-v", "--record-value", type=str, metavar='', help="Value of domain record: IP address for A or AAAA record, or FQDN for CNAME alias")
cf_create_subparser.add_argument("-t", "--record-type", type=str, choices=["a", "aaaa", "cname"], help="Type of domain record to create")

# Delete modules
cf_delete_subparser = cf_actions_subparser.add_parser(name="delete", formatter_class=formatter, help="Delete a domain record")
cf_delete_subparser.add_argument("-k", "--api-key", action="store_true", help="Enter Cloudflare API token when requested")
cf_delete_subparser.add_argument("-d", "--domain", type=str, metavar='', help="Deletes records from target domain")
cf_delete_subparser.add_argument("-n", "--record-name", type=str, metavar='', help="Name of domain record to delete")

cf_list_domains = cf_actions_subparser.add_parser(name="list", formatter_class=formatter, help="List current domain records")
cf_list_domains.add_argument("-k", "--api-key", action="store_true", help="Enter Cloudflare API token when requested")

# Porkbun options
porkbun_subparser = dns_registrar_subparser.add_parser(name="porkbun", formatter_class=formatter, help="Manage DNS records via Porkbun")
pb_actions_subparser = porkbun_subparser.add_subparsers(title="DNS Actions", dest="dns_action", description="Specify what operation to perform")

# Creation actions
pb_create_subparser = pb_actions_subparser.add_parser(name="create", formatter_class=formatter, help="Create a new domain record")
pb_create_subparser.add_argument("-k", "--api-key", action="store_true", help="Enter the Porkbun API key when requested")
pb_create_subparser.add_argument("-s", "--secret-key", action="store_true", help="Enter the Porkbun secret key when requested")
pb_create_subparser.add_argument("-d", "--domain", type=str, metavar='', help="Creates new records in target domain")
pb_create_subparser.add_argument("-n", "--record-name", type=str, metavar='', help="Name of new domain record")
pb_create_subparser.add_argument("-v", "--record-value", type=str, metavar='', help="Value of domain record: IP address for A or AAAA record, or FQDN for CNAME alias")
pb_create_subparser.add_argument("-t", "--record-type", type=str, choices=["a", "aaaa", "cname"], help="Type of domain record to create")

# Deletion actions
pb_delete_subparser = pb_actions_subparser.add_parser(name="delete", formatter_class=formatter, help="Delete a domain record")
pb_delete_subparser.add_argument("-k", "--api-key", action="store_true", help="Enter the Porkbun API key when requested")
pb_delete_subparser.add_argument("-s", "--secret-key", action="store_true", help="Enter the Porkbun secret key when requested")
pb_delete_subparser.add_argument("-d", "--domain", type=str, metavar='', help="Deletes records from target domain")
pb_delete_subparser.add_argument("-n", "--record-name", type=str, metavar='', help="Name of domain record to delete")

pb_list_domains = pb_actions_subparser.add_parser(name="list", formatter_class=formatter, help="List current domain records")
pb_list_domains.add_argument("-k", "--api-key", action="store_true", help="Enter the Porkbun API key when requested")
pb_list_domains.add_argument("-s", "--secret-key", action="store_true", help="Enter the Porkbun secret key when requested")


# Redirector config
redir_subparser = redir_parser.add_subparsers(title="Redirector Actions", dest="redir_action", description="Manage redirectors")
create_redir_subparser = redir_subparser.add_parser(name="create", formatter_class=formatter, help="Create a new redirector")
cloud_create_redir_subparser = create_redir_subparser.add_subparsers(title="cloud", dest="cloud", description="Specify which cloud provider you'd like to build a redirector in")

aws_create_redir_subparser = cloud_create_redir_subparser.add_parser(name="aws", formatter_class=formatter, help="Create a redirector in AWS")
aws_create_redir_subparser.add_argument("-a", "--access-key", action="store_true", help="Enter the AWS access key when requested")
aws_create_redir_subparser.add_argument("-s", "--secret-key", action="store_true", help="Enter the AWS secret key when requested")
aws_create_redir_subparser.add_argument("-S", "--size", required=True, type=str, choices=["t2.micro", "t2.small", "t2,medium", "t3.micro", "t3.small", "t3.medium"], help="Size of redirector EC2")
aws_create_redir_subparser.add_argument("-r", "--region", type=str, help="Create redirector in target AWS region")
aws_create_redir_subparser.add_argument("-o", "--os", required=True, type=str, choices=["debian", "ubuntu"], help="Specify OS for the redirector")


delete_redir_subparser = redir_subparser.add_parser(name="delete", formatter_class=formatter, help="Delete a redirector")
cloud_delete_redir_subparser = delete_redir_subparser.add_subparsers(title="cloud", dest="cloud", description="Specify which cloud provider to decommission Gaia-created redirector infrastructure in")
aws_delete_redir_subparser = cloud_delete_redir_subparser.add_parser(name="aws", formatter_class=formatter, help="Delete Gaia redirector infrastructure from AWS")

certbot_redir_subparser = redir_subparser.add_parser(name="certbot", formatter_class=formatter, help="Install Certbot and enable HTTPS on a redirector")
certbot_redir_subparser.add_argument("-d", "--domain", required=True, type=str, metavar='', help="FQDN for target website to request TLS certificates")
certbot_redir_subparser.add_argument("-S", "--redirector-server", required=True, type=str, metavar='', help="Hostname or IP address of target server to execute certbot")
certbot_redir_subparser.add_argument("-u", "--redirector-user", required=True, type=str, metavar='', help="User to authenticate as over SSH on target server")
certbot_redir_subparser.add_argument("-P", "--password", type=str, metavar='', help="SSH user password or SSH key passphrase")
certbot_redir_subparser.add_argument("-i", "--identity-file", type=str, metavar='path/to/file', help="SSH key for authentication")
certbot_redir_subparser.add_argument("--stderr", action="store_true", help="Show stderr from install steps from target server after stdout")

rules_redir_subparser = redir_subparser.add_parser(name="generate", formatter_class=formatter, help="Generate redirector rules based on existing payload in Mythic and upload them to redirector")
rules_redir_subparser.add_argument("-u", "--payload-uuid", required=True, type=str, metavar='', help="UUID of payload to use as the basis of apache mod_rewrite rule generation")
rules_redir_subparser.add_argument("-t", "--redirect-target", required=True, type=str, metavar='', help="URL of website to redirect non-c2 traffic to")
rules_redir_subparser.add_argument("-rS", "--redir-server", required=True, type=str, metavar='', help="Hostname or IP address of redirector server")
rules_redir_subparser.add_argument("-ru", "--redir-ssh-user", required=True, type=str, metavar='', help="User to authenticate as over SSH on redirector server")
rules_redir_subparser.add_argument("-rp", "--redir-ssh-password", type=str, metavar='', help="Redirector SSH user password or SSH key passphrase")
rules_redir_subparser.add_argument("-ri", "--redir-ssh-identity-file", type=str, metavar='path/to/file', help="SSH key for authentication")

tunnel_redir_subparser = redir_subparser.add_parser(name="tunnel", formatter_class=formatter, help="Configure SSH tunnel between Mythic server and redirector")
tunnel_redir_subparser.add_argument("-mS", "--mythic-server", required=True, type=str, metavar='', help="Hostname or IP address of Mythic server")
tunnel_redir_subparser.add_argument("-mP", "--mythic-ssh-port", default=22, type=int, metavar='', help="SSH port for Mythic server")
tunnel_redir_subparser.add_argument("-mu", "--mythic-ssh-user", required=True, type=str, metavar='', help="User to authenticate as over SSH on redirector server")
tunnel_redir_subparser.add_argument("-mp", "--mythic-ssh-password", type=str, metavar='', help="Mythic SSH user password or SSH key passphrase")
tunnel_redir_subparser.add_argument("-mi", "--mythic-ssh-identity-file", type=str, metavar='path/to/file', help="SSH key for authentication")
tunnel_redir_subparser.add_argument("-rS", "--redir-server", required=True, type=str, metavar='', help="Hostname or IP address of redirector server")
tunnel_redir_subparser.add_argument("-ru", "--redir-ssh-user", required=True, type=str, metavar='', help="User to authenticate as over SSH on redirector server")

args = global_parser.parse_args()
##################################################################  END CLI PARSING ##################################################################


async def main():
    # If gaia runs on its own without args, print help
    if args.subcommand == None:
        global_parser.print_help()
        sys.exit(1)

    # Copy .env template to .env
    if os.path.isfile(".env-template") == True and os.path.isfile(".env") == False:
        shutil.copy(".env-template", ".env")

    # Install Mythic on designated system
    if args.subcommand == "install":
        import paramiko, utils.install

        # Initialize SSH
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Get connection information
        server = args.server
        port = args.port
        user = args.user
        display_stderr = args.stderr
        ssh_key = args.identity_file

        # Ready password or ssh passphrase
        if args.password == True:
            password = getpass.getpass()
        else:
            password = None
            
        # Paramiko attempts SSH key auth first, then password as a fallback
        ssh.connect(hostname=server, port=port, username=user, key_filename=ssh_key, password=password, look_for_keys=True, allow_agent=True)

        
        # Update system if requested
        if args.install_updates == True:
            print("###########################")
            print("# Updating remote system! #")
            print("###########################")
            (stdin, stdout, stderr) = ssh.exec_command("sudo apt update && sudo apt upgrade -y")
            utils.install.print_terminal_output(stdout)

            if display_stderr == True:
                # Print errors so user is aware if there are any
                utils.install.print_terminal_output(stderr)

        # Install dependencies if requested
        if args.install_deps == True:
            print("###########################")
            print("# Installing Dependencies #")
            print("###########################")
            utils.install.convert_line_endings("install_deps.sh")
            utils.install.copy_and_execute_script(ssh=ssh, script="install_deps.sh", err=display_stderr)

        # Install Mythic
        if args.install_mythic == True:
            print("#####################################################################")
            print("# Installing Mythic. This will take a while, so go get some coffee. #")
            print("#####################################################################")
            utils.install.convert_line_endings("install_mythic.sh")
            utils.install.copy_and_execute_script(ssh=ssh, script="install_mythic.sh", err=display_stderr)

            # Get mythic admin password
            stdin, stdout, stderr = ssh.exec_command("grep 'MYTHIC_ADMIN_PASSWORD' /opt/Mythic/.env")
            mythic_admin_password = stdout.readlines()
            mythic_admin_password = mythic_admin_password[0].split('"')
            mythic_admin_password = mythic_admin_password[1]

            print("#######################################")
            print("# Dumping mythic creds to local disk! #")
            print("#######################################")
            with open("mythic_admin_creds.txt", "w") as file:
                mythic_admin_creds = "mythic_admin:" + mythic_admin_password
                file.write(mythic_admin_creds)

            print("NOTE: If the password for `mythic_admin` is lost, run `grep \"MYTHIC_ADMIN_PASSWORD\" /opt/Mythic/.env | cut -d \'\"\' -f 2` on the server mythic is installed on.")

        ssh.close()
        sys.exit(0)

    # Import Mythic auth early for functions that require it
    import utils.auth

    # Handles authentication to Mythic
    if args.subcommand == "auth":
        import utils.env
        
        # Authenticates to mythic if server, port, user, and password are specified
        auth_user = args.user
        mythic_host = args.server
        mythic_port = args.port

        if args.password == True:
            auth_password = getpass.getpass()

        # Auth according to SSL input
        if args.no_ssl == False:
            mythic_session = await utils.auth.mythic_login_with_user_creds(username=auth_user, password=auth_password, server_host=mythic_host, server_port=mythic_port)
        elif args.no_ssl == True:
            mythic_session = await utils.auth.mythic_login_with_user_creds_no_ssl(username=auth_user, password=auth_password, server_host=mythic_host, server_port=mythic_port)
        else:
            print("Unknown error in SSL processing during mythic authentication flow.")
            sys.exit(1)

        # Create an API key for the current user
        api_token = await utils.auth.mythic_get_api_token(mythic_instance=mythic_session)    

        # Dumps API key and mythic connection information into .env
        utils.env.update_env("MYTHIC_LOGIN_SERVER_HOST", mythic_host)
        utils.env.update_env("MYTHIC_LOGIN_SERVER_PORT", str(mythic_port))
        utils.env.update_env("MYTHIC_API_KEY", api_token)

        print("Mythic authentication successful!")
        sys.exit(0)

    # Handles DNS management
    if args.subcommand == "dns":
        import utils.env

        if args.registrar == "cloudflare":
            # Validate that we have the CF API key
            import utils.dns.cf

            # Pull API key from env
            if args.api_key == False:
                api_token = config["CLOUDFLARE_API_TOKEN"]

            # Sepcify API key
            elif args.api_key == True:
                api_token = getpass.getpass("Cloudflare API Key: ")

            # Update env file with API key
            if api_token != None:
                utils.env.update_env(env_key="CLOUDFLARE_API_TOKEN", env_value=api_token)
            else:
                print("Specify a Cloudflare API Key with --api-key or in .env.")
                sys.exit(1)

            # Print active domains
            if args.dns_action == "list":
                # Get the domains listed in the account
                domains = utils.dns.cf.get_domains(api_token=api_token)

                # Print active domains
                print("Active domains:")
                for i in domains["result"]:
                    if i["status"] == "active":
                        print(i["name"])

                sys.exit(0)


            if args.dns_action == "create":
                domain = args.domain
                record_name = args.record_name
                record_value = args.record_value
                record_type = args.record_type
                domain_id = None
                

                # Get the domains listed in the account
                domains = utils.dns.cf.get_domains(api_token=api_token)
                
                # Check that our specified domain returns from this account
                for i in domains["result"]:
                    if i["name"] == domain:
                        domain_id = i["id"]
                        break                  

                # Make sure that the domain returned
                if domain_id == None:
                    print("Please specify a valid domain.")
                    sys.exit(1)

                # Get the current dns records for the given domain
                records = utils.dns.cf.get_domain_records(api_token=api_token, zone_id=domain_id)

                target_fqdn = f"{record_name}.{domain}"
                
                # Compare records with the intended incoming record, skip creation if it exists. Delete the record if specified.
                if records["result"] != []:
                    for i in records["result"]:

                        # Split out some of the domain parameters for easier debugging
                        existing_record_name = i["name"]

                        # Allow for -n to only need the key rather than FQDN
                        target_fqdn = f"{record_name}.{domain}"

                        # Exit if there is a domain record name conflict
                        if existing_record_name == target_fqdn:
                            print("New record name conflicts with existing record.")
                            sys.exit(1)
                        
                    # If domain record does not exist and we are trying to create a new record, create it.
                    record_create = utils.dns.cf.create_domain_record(api_token=api_token, zone_id=domain_id, record_name=record_name, record_type=record_type, record_target=record_value)
                    print("Created requested domain record.")

                else:
                    # Create the record if there are no pre-existing domain records
                    record_create = utils.dns.cf.create_domain_record(api_token=api_token, zone_id=domain_id, record_name=record_name, record_type=record_type, record_target=record_value)
                    print("Created requested domain record.")

                sys.exit(0)

            if args.dns_action == "delete":
                domain_id = None
                domain = args.domain
                record_name = args.record_name                

                # Get the domains listed in the account
                domains = utils.dns.cf.get_domains(api_token=api_token)
                
                # Check that our specified domain returns from this account
                for i in domains["result"]:
                    if i["name"] == domain:
                        domain_id = i["id"]
                        break                   

                # Make sure that the domain returned
                if domain_id == None:
                    print("Please specify a valid domain.")
                    sys.exit(1)

                # Get the current dns records for the given domain
                records = utils.dns.cf.get_domain_records(api_token=api_token, zone_id=domain_id)
                if records["result"] != []:
                    for i in records["result"]:

                        # Split out some of the domain parameters for easier debugging
                        existing_record_name = i["name"]
                        existing_record_id = i["id"]

                        # Allow for -n to only need the key rather than FQDN
                        target_fqdn = f"{record_name}.{domain}"

                        # Exit if there is a domain record name conflict
                        if existing_record_name == target_fqdn:
                            utils.dns.cf.delete_domain_record(api_token=api_token, zone_id=domain_id, dns_record_id=existing_record_id)
                            print("Domain record deleted.")
                            sys.exit(0)

                    print("No matching records to delete.")
                    sys.exit(1)
                else:
                    print("No records to delete.")
                    sys.exit(1)


        if args.registrar == "porkbun":
            import utils.dns.porkbun
            domain_id = None

            # Pull Porkbun API from env
            if args.api_key == False:
                api_pk1 = config["PORKBUN_API_KEY"]

            # Sepcify API key
            elif args.api_key == True:
                api_pk1 = getpass.getpass("Porkbun API Key: ")

            # Update env file with API key
            if api_pk1 != '':
                utils.env.update_env(env_key="PORKBUN_API_KEY", env_value=api_pk1)
            else:
                print("Specify a Porkbun API Key with --api-key or in .env.")
                sys.exit(1)
            
            # Pull Porkbun secret from env
            if args.secret_key == False:
                api_sk1 = config["PORKBUN_SECRET_KEY"]

            # Sepcify Secret key
            elif args.secret_key == True:
                api_sk1 = getpass.getpass("Porkbun Secret Key: ")

            # Update env file with API key
            if api_sk1 != '':
                utils.env.update_env(env_key="PORKBUN_SECRET_KEY", env_value=api_sk1)
            else:
                print("Specify a Porkbun Secret Key with --secret-key or in .env.")
                sys.exit(1)

            if args.dns_action == "list":
                domains = utils.dns.porkbun.get_domains(api_pk1, api_sk1)

                # Print active domains
                print("Active domains:")
                for i in domains["domains"]:
                    if i["status"] == "ACTIVE":
                        print(i["domain"])

                sys.exit(0)


            if args.dns_action == "create":
                target_domain = None
                domain = args.domain
                record_name = args.record_name
                record_value = args.record_value
                record_type = args.record_type

                # Get the domains listed in the account
                domains = utils.dns.porkbun.get_domains(api_pk1, api_sk1)

                # Check that our specified domain returns from this account
                for i in domains["domains"]:
                    if i["domain"] == domain:
                        target_domain = i["domain"]
                        break
                    
                if target_domain == None:
                    print("Please specify a valid domain.")
                    sys.exit(1)

                # Get the current dns records
                records = utils.dns.porkbun.get_domain_records(api_key=api_pk1, secret_key=api_sk1, domain=target_domain)

                # Required because porkbun wants to specify the record name without the rest of the domain
                target_fqdn = f"{record_name}.{target_domain}"

                # Compare records with the intended incoming record, skip creation if it exists. Delete the record if specified.
                for i in records["records"]:
                    if i["name"] == target_fqdn:
                        print("New record name conflicts with existing record.")
                        sys.exit(1)

                # Catch Porkbun quirk of wanting an empty string for a root domain object
                if target_domain == record_name or record_name == "@" or record_name == "":
                    record_name = ""

                record_create = utils.dns.porkbun.create_domain_record(api_key=api_pk1, secret_key=api_sk1, domain=target_domain, record_name=record_name, record_type=record_type, record_target=record_value)
                print("Created requested domain record.")
                sys.exit(0)

            if args.dns_action == "delete":
                target_domain = None
                domain = args.domain
                record_name = args.record_name

                # Get the domains listed in the account
                domains = utils.dns.porkbun.get_domains(api_pk1, api_sk1)

                # Check that our specified domain returns from this account
                for i in domains["domains"]:
                    if i["domain"] == domain:
                        target_domain = i["domain"]
                        break
                    
                if target_domain == None:
                    print("Please specify a valid domain.")
                    sys.exit(1)

                # Get the current dns records
                records = utils.dns.porkbun.get_domain_records(api_key=api_pk1, secret_key=api_sk1, domain=target_domain)

                # Required because porkbun wants to specify the record name without the rest of the domain
                target_fqdn = f"{record_name}.{target_domain}"

                # Compare records with the intended incoming record, skip creation if it exists. Delete the record if specified.
                for i in records["records"]:
                    if i["name"] == target_fqdn:
                        record_id = i["id"]
                        utils.dns.porkbun.delete_domain_record_by_id(api_key=api_pk1, secret_key=api_sk1, domain=target_domain, record_id=record_id)
                        print("Successfully deleted specified domain record.")
                        sys.exit(0)

                print("No matching records to delete.")
                sys.exit(1)

    # Check if config has been changed, if not then env has not been loaded.
    if config["MYTHIC_API_KEY"] == "":
        print("No Mythic API key detected in .env. Have you authenticated to Mythic?")
        auth_parser.print_help()
        sys.exit(1)

    # Authenticates to mythic with API key if auth is not specified
    api_key = config["MYTHIC_API_KEY"]
    mythic_host = config["MYTHIC_LOGIN_SERVER_HOST"]
    mythic_port = config["MYTHIC_LOGIN_SERVER_PORT"]
    mythic_session = await utils.auth.mythic_login_with_api(api_token=api_key, server_host=mythic_host, server_port=mythic_port)
    
    # Handles creation and destruction of redirectors
    if args.subcommand == "redirector":
        import utils.redirector, paramiko, utils.install, utils.env
        if args.redir_action == "create":
            if args.cloud == "aws":
                import boto3

                if config["AWS_ACCESS_KEY_ID"] != "":
                    aws_access_key = config["AWS_ACCESS_KEY_ID"]
                else :
                    aws_access_key = getpass.getpass("AWS Access Key: ")
                    # Fix env

                if config["AWS_SECRET_ACCESS_KEY"] != "":
                    aws_secret_key = config["AWS_SECRET_ACCESS_KEY"]
                else :
                    aws_secret_key = getpass.getpass("AWS Secret Key: ")
                    # fix env

                if config["AWS_DEFAULT_REGION"] != "":
                    aws_region = config["AWS_DEFAULT_REGION"]
                else :
                    aws_region = args.region
                    # fix env

                ec2_size = args.size

                # Connect to EC2 Service
                print("Connecting to AWS")
                aws_session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
                ec2_client = aws_session.client("ec2")   

                # Specify OS for redirector EC2
                if args.os == "ubuntu":
                    ec2_os = "ubuntu"
                    ec2_user = "ubuntu"
                    # Add these to env

                elif args.os == "debian":
                    ec2_os = "debian"
                    ec2_user = "admin"

                # Create EC2 key pair
                print("Creating gaia-redir keypair for EC2")
                aws_key_name = utils.redirector.create_aws_key_pair(ec2_session=ec2_client, key_name="gaia-redir")
                home_dir = os.path.expanduser("~")
                ssh_dir = f"{home_dir}/.ssh/"
                aws_key_name_local_path = f"{ssh_dir}/{aws_key_name}.pem"

                # Creates security group
                print("Creating EC2 Security Group.")
                aws_security_group_id = utils.redirector.create_aws_security_group(ec2_session=ec2_client)

                # Allows http, https, and ssh inbound
                print("Allowing SSH, HTTP, and HTTPS into EC2 Instance.")
                utils.redirector.create_aws_security_group_entry(ec2_session=ec2_client, security_group_id=aws_security_group_id, transport_protocol="tcp", port=80)
                utils.redirector.create_aws_security_group_entry(ec2_session=ec2_client, security_group_id=aws_security_group_id, transport_protocol="tcp", port=443)
                utils.redirector.create_aws_security_group_entry(ec2_session=ec2_client, security_group_id=aws_security_group_id, transport_protocol="tcp", port=22)

                # Build EC2
                print("Launching EC2.")
                instance = utils.redirector.launch_ec2(ec2_session=ec2_client, os=ec2_os, ec2_size=ec2_size, key_name=aws_key_name, security_group_id=aws_security_group_id)
                instance_id = instance["Instances"][0]["InstanceId"]
                interface_id = instance["Instances"][0]["NetworkInterfaces"][0]["NetworkInterfaceId"]

                print("Sleeping for 60 seconds to allow EC2 to provision VM.")
                time.sleep(60)
                
                # Query for public IP address
                print("Grabbing instance's public IP.")
                interface_info = utils.redirector.get_aws_network_interface_public_ip(ec2_session=ec2_client, interface_id=interface_id)
                instance_public_ip = interface_info["NetworkInterfaces"][0]["Association"]["PublicIp"]

                # Initialize SSH
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Update EC2s
                print("Connecting to EC2 instance over SSH.")
                ssh.connect(hostname=instance_public_ip, port=22, username=ec2_user, key_filename=aws_key_name_local_path)
                print("Updating EC2 before rebooting.")
                (stdin, stdout, stderr) = ssh.exec_command("sudo apt update && sudo apt upgrade -y && sudo reboot")
                utils.install.print_terminal_output(stdout)
                ssh.close()

                print("Sleep for 60 more seconds to allow the VM to reboot and load new kernel")
                time.sleep(60)

                # Save the public IP for the redirector
                utils.env.update_env("REDIRECTOR_PUBLIC_IP", instance_public_ip)

                print("Reconnecting to EC2 before installing apache2")
                ssh.connect(hostname=instance_public_ip, port=22, username=ec2_user, key_filename=aws_key_name_local_path)

                # Install and perform initial configuration of apache from the shell script
                print("Installing and configuring Apache2")
                utils.install.convert_line_endings("install_apache.sh")
                utils.install.copy_and_execute_script(ssh=ssh, script="install_apache.sh", err=False)

                ssh.close()
                sys.exit(0)

        if args.redir_action == "delete":
            if args.cloud == "aws":
                import boto3

                instance_ids, ssh_key_ids, security_group_ids = [], [], []

                aws_session = boto3.Session(aws_access_key_id=config["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"], region_name=config["AWS_DEFAULT_REGION"])
                ec2_client = aws_session.client("ec2")  

                # Query for EC2s with gaia tags on them
                print("Getting Gaia EC2s from AWS")
                ec2_info = utils.redirector.get_gaia_ec2s(ec2_session=ec2_client)
                
                # Collect instnace IDs and append them to a list to pass to deletion function later
                for i in ec2_info["Reservations"]:
                    for j in i["Instances"]:
                        instance_ids.append(j["InstanceId"])

                # Query for ssh keys with gaia tags on them
                print("Getting Gaia SSH keys from AWS.")
                keypair_info = utils.redirector.get_gaia_key_pairs(ec2_session=ec2_client)
                for i in keypair_info["KeyPairs"]:
                    ssh_key_ids.append(i["KeyPairId"])

                # Query for security groups with gaia tags on them
                print("Getting Gaia Security Groups from AWS.")
                security_group_info = utils.redirector.get_gaia_security_groups(ec2_session=ec2_client)
                for i in security_group_info["SecurityGroups"]:
                    security_group_ids.append(i["GroupId"])

                # Terminate Gaia instances
                print("Terminating Gaia related EC2 instances.")
                terminate = utils.redirector.terminate_gaia_instances(ec2_session=ec2_client, instance_ids=instance_ids)
                print("Sleeping for 2 minutes to allow EC2 instances to terminate.")
                time.sleep(120)

                # Delete Gaia SSH Keys
                print("Deleting Gaia SSH Keys within EC2.")
                for i in ssh_key_ids:
                    key_delete = utils.redirector.delete_gaia_ssh_keys(ec2_session=ec2_client, key_pair_id=i)
                    if key_delete["Return"] == False:
                        print("Key delete failed, trying agian after 30 seconds.")
                        time.wait(30)
                        key_delete = utils.redirector.delete_gaia_ssh_keys(ec2_session=ec2_client, key_pair_id=i)
                        if key_delete["Return"] == False:
                            print("Key deletion failed again, retry later.")
                            continue

                # Delete local copy of ssh key
                print("Deleting local copy of SSH key for Gaia.")
                utils.redirector.delete_local_gaia_ssh_key("gaia-redir")

                # Delete Gaia Security groups
                print("Deleting Gaia Security Groups.")
                for i in security_group_ids:
                    group_delete = utils.redirector.delete_gaia_security_groups(ec2_session=ec2_client, group_id=i)
                    if group_delete["Return"] == False:
                        print("Security Group delete failed, trying agian after 30 seconds.")
                        time.wait(30)
                        group_delete = utils.redirector.delete_gaia_security_groups(ec2_session=ec2_client, group_id=i)
                        if group_delete["Return"] == False:
                            print("Security Group deletion failed again, retry later.")
                            continue

                print("Gaia cleanup complete!")
                sys.exit(0)
    
        # Handles configuration of certbot
        if args.redir_action == "certbot":
            import paramiko, utils.install

            # Get domain to activate certbot on
            certbot_domain = args.domain

            # Initialize SSH
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Get connection information
            server = args.redirector_server
            user = args.redirector_user

            # Determine if we show stderr on streamed terminal output
            if args.stderr == True:
                display_stderr = True
            else:
                display_stderr = False

            # Ready SSH key if one is specified
            if args.identity_file != None:
                ssh_key = args.identity_file.strip()
            else:
                ssh_key = None

            # Ready password or ssh passphrase
            if args.password == True:
                password = getpass.getpass()
            else:
                password = None
                
            print("Connecting to redirector.")
            # Paramiko attempts SSH key auth first, then password as a fallback
            ssh.connect(hostname=server, port=22, username=user, key_filename=ssh_key, password=password, look_for_keys=True, allow_agent=True)

            # Configures certbot
            print("Running certbot.")
            (stdin, stdout, stderr) = ssh.exec_command(f"sudo certbot run -n --apache --agree-tos -d {certbot_domain}")
            utils.install.print_terminal_output(stdout)

            ssh.close()
            sys.exit(0)

        if args.redir_action == "generate":
            payload_uuid = args.payload_uuid
            redirector_server = args.redir_server
            redirector_server_user = args.redir_ssh_user
            redirect_target = args.redirect_target

            if args.redir_ssh_password == True:
                redirector_ssh_password = getpass.getpass("Redirector User SSH Password")
            else:
                redirector_ssh_password = None

            if args.redir_ssh_identity_file != None:
                redirector_ssh_key = args.redir_ssh_identity_file
            else:
                redirector_ssh_key = None

            # Query for mod_rewrite rules
            print("Generating base redirector rules.")
            redirector_rules_line = await utils.redirector.generate_redirector_rules(mythic_instance=mythic_session, payload_uuid=payload_uuid)

            # Modify mod_rewrite rules so they work as expected
            print("Modifying redirector rules to ensure they work with given parameters.")
            redirector_rules = redirector_rules_line["redirect_rules"]["output"].split("\n")
            for i in range(len(redirector_rules)):
                if "http://C2_SERVER_HERE:80" in redirector_rules[i]:
                    redirector_rules[i] = redirector_rules[i].replace("http://C2_SERVER_HERE:80", f"http://localhost:8443")
                elif "redirect/?" in redirector_rules[i]:
                    redirector_rules[i] = redirector_rules[i].replace("redirect/?", f"\"{redirect_target}\"")
                
                redirector_rules[i] = redirector_rules[i] + '\n'

            # Write .htaccess file
            print("Saving redirector rules on disk as .htaccess.")
            with open (".htaccess", "w") as file:
                file.writelines(redirector_rules)

            # Upload mod_rewrite rules to the redirector and reboot apache
            # Initialize SSH for redirector
            redir_tunnel = paramiko.SSHClient()
            redir_tunnel.load_system_host_keys()
            redir_tunnel.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print("Connecting to redirector.")
            redir_tunnel.connect(hostname=redirector_server, port=22, username=redirector_server_user, password=redirector_ssh_password, key_filename=redirector_ssh_key, allow_agent=True, look_for_keys=True)
            
            print("Copying .htaccess to redirector.")
            utils.install.copy_file(ssh=redir_tunnel, file=".htaccess")

            print("Moving .htaccess to /var/www/html/ and reloading apache.")
            (stdin, stdout, stderr) = redir_tunnel.exec_command("sudo cp .htaccess /var/www/html/.htaccess && sudo chmod 644 /var/www/html/.htaccess && sudo systemctl restart apache2")
            utils.install.print_terminal_output(stdout)

            print("Redirector file successfully configured!")
            redir_tunnel.close()
            sys.exit(0)

        if args.redir_action == "tunnel":
            import paramiko, utils.redirector, utils.payloads, utils.install

            mythic_server = args.mythic_server
            mythic_server_user = args.mythic_ssh_user
            mythic_ssh_port = args.mythic_ssh_port

            if args.mythic_ssh_identity_file != None:
                mythic_ssh_key = args.mythic_ssh_identify_file
            else:
                mythic_ssh_key = None

            if args.mythic_ssh_password == True:
                mythic_ssh_password = getpass.getpass("Mythic SSH User Password:")
            else:
                mythic_ssh_password = None

            # Redirector server connection information
            redirector_server = args.redir_server
            redirector_server_user = args.redir_ssh_user
            
            # Create the SSH tunnel to the redirector
            # Initialize SSH for redirector
            mythic_tunnel = paramiko.SSHClient()
            mythic_tunnel.load_system_host_keys()
            mythic_tunnel.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print("Connecting to Mythic server.")
            mythic_tunnel.connect(hostname=mythic_server, port=mythic_ssh_port, username=mythic_server_user, password=mythic_ssh_password, key_filename=mythic_ssh_key, allow_agent=True, look_for_keys=True)

            print("Copying Gaia-created SSH key for redirector to Mythic server.")
            utils.install.copy_gaia_ssh_key(ssh=mythic_tunnel)
            (stdin, stdout, stderr) = mythic_tunnel.exec_command(f"chmod 600 ~/.ssh/gaia-redir.pem")

            print("Creating systemd service file to build SSH tunnel on redirector.")
            with open("utils/redirector-tunnel-key.service", "r") as file:
                service = file.readlines()

            print("Modifying systemd service file with specified parameters.")
            for i in range(len(service)):
                if "user@example.com" in service[i]:
                    service[i] = service[i].replace("user@example.com", f"{redirector_server_user}@{redirector_server}")
                    service[i] = service[i].replace("/home/example/.ssh/gaia-redir.pem", f"/home/{mythic_server_user}/.ssh/gaia-redir.pem")
                if "User=" in service[i]:
                    service[i] = service[i].replace("User=\n", f"User={mythic_server_user}\n")
                    
            print("Saving modified systemd service file on disk before sending it to Mythic server.")
            with open("redirector-tunnel.service", "w") as file:
                file.writelines(service)

            print("Copying finished systemd service file to Mythic server, enabling the new service, and building the SSH tunnel to redirector.")
            utils.install.copy_file(ssh=mythic_tunnel, file="redirector-tunnel.service")
            mythic_tunnel.exec_command("sudo cp redirector-tunnel.service /etc/systemd/system/redirector-tunnel.service")
            mythic_tunnel.exec_command("sudo chown root:root /etc/systemd/system/redirector-tunnel.service")
            mythic_tunnel.exec_command("sudo chmod 644 /etc/systemd/system/redirector-tunnel.service")
            mythic_tunnel.exec_command("sudo systemctl daemon-reload")
            mythic_tunnel.exec_command("sudo systemctl start redirector-tunnel.service")
            mythic_tunnel.exec_command("sudo systemctl enable redirector-tunnel.service")

            print("SSH tunnel and service successfully created!")
            mythic_tunnel.close()
            sys.exit(0)

    # Manages users
    if args.subcommand == "user":
        import utils.users, utils.operations

        users_stdin = args.users
        stdout = args.cred_stdout
        # operation = args.operation

        # Ready user list as input and prepares for merge later
        if args.user_list:
            print("Reading user list from file.")
            user_list_in = args.user_list.strip()
        else:
            user_list_in = []

        # Ready user credentials list for output
        if args.cred_file:
            user_list_out = args.cred_file.strip()
            cred_list = []
        else:
            cred_list = None

        # Take users from stdin and list, merge, deduplicate, and prepare for passing to mythic
        print("Merging user file and cli specified users into a single list.")
        users = utils.users.prepare_users(users_stdin=users_stdin, user_file_in=user_list_in)
        
        # Create new users before assigning them to default operation (The first opeation that returns when getting all operations)
        if args.user == "create":
            
            print("Creating new Mythic users.")
            for i in users:
                user_creds = await utils.users.create_user(mythic_instance=mythic_session, username=i)
                
                # Print creds if user specifies to
                if stdout == True:
                    print(user_creds)

                # Append creds to a list to prepare to dump to file if user specifies to
                if cred_list != None:
                    user_creds = user_creds + '\n'
                    cred_list.append(user_creds)

            # Dump creds to file
            if cred_list != None:
                print("Dumping new Mythic user credentials to disk.")
                with open(user_list_out, 'a') as file:
                    file.writelines(cred_list)
                
    # if args.user == "delete":
    #     pass    
    
    # if args.user == "assign":
    #     # Get current operations to prepare to assign a default for a new user
    #     await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=operation, username=i)

    # if args.user == "list":
    #     pass

        sys.exit(0)

    # Process operations
    if args.subcommand == "operation":
        import utils.operations, utils.env

        if args.operation == "list":
            operations = await utils.operations.get_operations(mythic_instance=mythic_session)
            print("Current operations in Mythic:")
            for i in operations:
                print(i)

        # Creates new operation
        if args.operation == "create":
            operation = args.name
            print(f"Creating new Operation: {operation}")
            await utils.operations.create_operation(mythic_instance=mythic_session, operation_name=operation)

            # Modify env to include new operation
            utils.env.update_env("MYTHIC_OPERATION_NAME", operation)

        # Assigns users to operations
        if args.operation == "assign":
            operation_name = args.operation_name
            users = args.users

            print("Assigning users to operation")
            for i in users:
                await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=operation_name, username=i)
                print(f"Assigned user {i} to operation {operation_name}")

        sys.exit(0)

    # Create payloads
    if args.subcommand == "payload":
        import utils.payloads
        if args.payloads == "create":
            import utils.env, datetime

            # Some spaghetti code incoming. If you know how to get args to play nice with a function, please tell me
            # Use specified callback url if one is supplied
            if args.callback_url:
                callback_url = args.callback_url
            
            # Otherwise use the value saved in env
            elif config['MYTHIC_HTTP_CALLBACK_URL_BASE'] != '' or config['MYTHIC_HTTP_CALLBACK_URL_BASE'] != '':
                callback_url = config['MYTHIC_HTTP_CALLBACK_URL_BASE']
            else:
                print("Ensure that a callback url is specified in either .env or passed via cli")
                payload_parser.print_help()
                sys.exit(1)

            # Update env file if requested or required
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_URL_BASE', env_value=callback_url)

            # Callback Ports
            # Use specified callback port if one is supplied
            if args.callback_port:
                callback_port = args.callback_port
            
            # Otherwise use the value saved in env
            elif config['MYTHIC_HTTP_CALLBACK_PORT'] != '' or config['MYTHIC_HTTP_CALLBACK_PORT'] != '':
                callback_port = config['MYTHIC_HTTP_CALLBACK_PORT']

            else:
                print("Ensure that a callback port is specified in either .env or passed via cli")
                payload_parser.print_help()
                sys.exit(1)

            # Update env file if requested or required
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_PORT', env_value=callback_port)

            # Callback Killdate
            # Use specified callback killdate if one is supplied
            if args.callback_killdate:
                callback_killdate = args.callback_killdate
            
            # Otherwise use the value saved in env
            elif config['MYTHIC_HTTP_CALLBACK_KILLDATE'] != '' or config['MYTHIC_HTTP_CALLBACK_KILLDATE'] != '':
                callback_killdate = config['MYTHIC_HTTP_CALLBACK_KILLDATE']
            
            # Otherwise use the default of a year
            else:
                callback_killdate_raw = datetime.date.today() + datetime.timedelta(days=365)
                callback_killdate = callback_killdate_raw.strftime("%Y-%m-%d")

            # Update env file if requested or required
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_KILLDATE', env_value=callback_killdate)

            payload_name_base = args.name

            # Process apollo payloads
            if args.agent == "apollo":
                # Generate normal executable
                print("Apollo portable executable building")
                payload_name_exe = payload_name_base + ".exe"
                await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="WinExe", payload_name=payload_name_exe, payload_description="Windows x64 .NET Framework Portable Executable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Apollo portable executable built")

                # Generate shellcode
                print("Apollo shellcode building")
                payload_name_bin = payload_name_base + ".bin"
                await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="Shellcode", payload_name=payload_name_bin, payload_description="Windows x64 Shellcode", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Apollo shellcode built")

                # Generate service executable
                print("Apollo service executable building")
                payload_name_svc = payload_name_base + "Svc.exe"
                await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="Service", payload_name=payload_name_svc, payload_description="Windows x64 .NET Framework Service Executable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Apollo service executable built")

                sys.exit(0)

            # process poseidon payloads
            if args.agent == "poseidon":
                payload_os = args.os.capitalize()

                if args.os == "linux":
                    # Generate linux x64 static elf
                    print("Poseidon linux x64 elf building")
                    await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="AMD_x64", payload_name=payload_name_base, static_linking="True", payload_description="Linux x64 Static ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Poseidon linux x64 elf built")

                    # Generate linux arm64 static elf
                    print("Poseidon linux arm64 elf building")
                    await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="ARM_x64", payload_name=payload_name_base, static_linking="True", payload_description="Linux arm64 Static ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Poseidon linux arm64 elf built")

                elif args.os == "macos":
                    # Translates to value poseidon builder expects
                    payload_os = "macOS"

                    # Generate macos arm64 static elf. macOS does not like static bins for some reason.
                    print("Poseidon macos x64 bin building")
                    await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="ARM_x64", payload_name=payload_name_base, static_linking="False", payload_description="macOS arm64 Static bin", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Poseidon macos x64 bin built")
        
                sys.exit(0)

            # Process athena payloads
            if args.agent == "athena":
                payload_os = args.os.capitalize()

                if args.os == "windows":
                    # Generate windows x64 .net portable executable
                    print("Athena windows x64 portable executable building")
                    payload_name_exe = payload_name_base + ".exe"
                    await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="x64", output_type="binary", payload_name=payload_name_exe, payload_description="Windows x64 .NET Portable Excutable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Athena windows x64 portable executable built")

                    # Generate windows x64 .net service executable
                    print("Athena windows x64 service executable building")
                    payload_name_svc = payload_name_base + "Svc.exe"
                    await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="x64", output_type="windows service", payload_name=payload_name_svc, payload_description="Windows x64 .NET Service Excutable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Athena windows x64 service executable built")
                
                elif args.os == "linux":
                    # Generate linux x64 .net elf
                    print("Athena linux x64 elf building")
                    await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="x64", output_type="binary", payload_name=payload_name_base, payload_description="Linux x64 .NET ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Athena linux x64 elf built")

                    # Generate linux arm64 .net elf
                    print("Athena linux arm64 elf building")
                    await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="arm64", output_type="binary", payload_name=payload_name_base, payload_description="Linux arm64 .NET ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Athena linux arm64 elf built")

                elif args.os == "macos":
                    # Translates to value athena builder expects
                    payload_os = "macOS"

                    # Generate macOS arm64 .net elf
                    print("Athena macos arm64 elf building")
                    await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="arm64", output_type="binary", payload_name=payload_name_base, payload_description="macOS arm64 .NET ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                    print("Athena macos arm64 elf built")

                sys.exit(0)

        if args.payloads == "list":
            payload_info = await utils.payloads.get_payloads(mythic_instance=mythic_session)
            print("Current Payloads:")
            for i in payload_info:
                if i["deleted"] == False:
                    payload_uuid = i["uuid"]
                    payload_type = i["payloadtype"]["name"]
                    payload_file_name = i["filemetum"]["filename_utf8"]
                    payload_description = i["description"]
                    payload_display = {
                        "payload_uuid" : payload_uuid,
                        "payload_type" : payload_type,
                        "payload_file_name" : payload_file_name,
                        "payload_description" : payload_description
                        }
                    print(payload_display)
                
        sys.exit(0)


if __name__ == '__main__':
     asyncio.run(main())

sys.exit(0)
