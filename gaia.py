import argparse, sys, os, asyncio, dotenv, getpass

# Load environment variables first
if os.path.isfile(".env"):
    config = dotenv.dotenv_values(".env")
else:
    config = None

#################################################################### CLI PARSING ####################################################################

# Root options that are available across the whole application
global_parser = argparse.ArgumentParser(
    prog='gaia.py',
    description='Lightweight tool to help install and manage mythic c2 for lab environments')

# 'Core' modules
subparsers = global_parser.add_subparsers(title='modules', help='', dest='subcommand')
auth_parser = subparsers.add_parser('auth', help='authenticates to mythic and dumps api key to .env')
dns_parser = subparsers.add_parser('dns', help='manage dns records')
install_parser = subparsers.add_parser('install', help='manages mythic installation components')
operation_parser = subparsers.add_parser('operations', help='manages mythic operations')
payload_parser = subparsers.add_parser('payloads', help='creates payloads')
user_parser = subparsers.add_parser('users', help='creates mythic users')

# Global modules
global_parser.add_argument('-k', '--no-ssl', action='store_true', help='disable ssl verification checks')
global_parser.add_argument('--update-env', action='store_true', help='overwrite .env file contents with specified cli args')

# Auth modules
auth_parser.add_argument('-S', '--server', required=True, nargs=1, metavar='', help="hostname, fqdn, or ip address for mythic server")
auth_parser.add_argument('-P', '--port', required=True, nargs=1, metavar='', help="port for web interface on mythic server")
auth_parser.add_argument('-p', '--password', required=True, nargs=1, metavar='', help='password for specified mythic user account')
auth_parser.add_argument('-u', '--username', required=True, nargs=1, metavar='', help='username for mythic authentication')

# User modules
action_user_parser = user_parser.add_mutually_exclusive_group(required=True)
user_parser.add_argument('-u', '--users', nargs='+', metavar='', help='specify one or more user account to process')
user_parser.add_argument('-l', '--user-list', nargs='?', metavar="path/to/user_list", help='pass user list via file')
user_parser.add_argument('-o', '--user-output', nargs='?', metavar='path/to/output', help='dumps newly created credentials to specified file')
action_user_parser.add_argument('-c', '--create', action='store_true', help='creates user accounts in mythic')
# action_user_parser.add_argument('-d', '--delete', action='store_true', help='deletes user accounts in mythic') 
user_parser.add_argument('-s', '--stdout', action='store_true', help='echos newly created creds to stdout')

# Operation modules
operation_parser.add_argument('-o', '--operation', required=True, nargs=1, metavar='', help='specifies operation to manage')
operation_parser.add_argument('-u', '--users', nargs='+', metavar='', help='specify one or more user account to process')
operation_parser.add_argument('-c', '--create', action='store_true', help='creates operations in mythic')

action_operation_parser = operation_parser.add_mutually_exclusive_group()
action_operation_parser.add_argument('-a', '--assign', action='store_true', help='assigns users to an operations')
action_operation_parser.add_argument('-r', '--remove', action='store_true', help='removes users from an operations')

# Payload Modules
agent_parser = payload_parser.add_mutually_exclusive_group(required=True)
agent_parser.add_argument('--apollo', action='store_true', help='builds apollo payloads')
agent_parser.add_argument('--athena', action='store_true', help='builds athena payloads')
agent_parser.add_argument('--poseidon', action='store_true', help='builds poseidon payloads')
payload_parser.add_argument('-n', '--name', nargs=1,  required=True, metavar='', help='base name of generated payloads before extensions are added')
payload_parser.add_argument('-U', '--callback-url', nargs=1, metavar='', help='specify url for agents to call back to')
payload_parser.add_argument('-P', '--callback-port', nargs=1, metavar='', help='specify port for agents to call back to')
payload_parser.add_argument('-K', '--callback-killdate', nargs=1, metavar='', help='specify when callbacks should be automatically terminated in yyyy-mm-dd format. Defaults to 1 year')
payload_parser.add_argument('-o', '--os', choices=['linux', 'macos', 'windows'], metavar='', help='specify operating system for athena and poseidon')

# Install Parser
install_parser.add_argument('-U', '--install-updates', action='store_true', help='update system with apt before installing mythic')
install_parser.add_argument('-D', '--install-deps', action='store_true', help='install dependencies on target host before installing mythic')
install_parser.add_argument('-M', '--install-mythic', action='store_true', help='install mythic on the target.')
install_parser.add_argument('-S', '--server', required=True, nargs=1, metavar='', help='specifies server to install mythic on')
install_parser.add_argument('-P', '--port', nargs=1, metavar='', help='port to connect to server over ssh')
install_parser.add_argument('-u', '--user', required=True, nargs=1, metavar='', help='user to connect to server over ssh')
install_parser.add_argument('-p', '--password', action='store_true', help='prompt for user password to authenticate or for use as ssh key passphrase')
install_parser.add_argument('-i', '--identity_file', nargs='?', metavar="path/to/user_list", help='provide path to ssh key')
install_parser.add_argument('-e', '--stderr', action='store_true', help='show stderr output from target server')

# DNS Parser
dns_record = dns_parser.add_mutually_exclusive_group(required=True)
dns_record.add_argument('--a', action='store_true', help='set an a record')
dns_record.add_argument('--cname', action='store_true', help='set a cname record')
dns_record.add_argument('--aaaa', action='store_true', help='set a aaaa record')
dns_parser.add_argument('-d', '--domain', required=True, metavar='', help='associate a record with a given domain or subdomain')
dns_parser.add_argument('-v', '--value', required=True, metavar='', help='assign a value to the domain record')
dns_parser.add_argument('-z', '--zone', required=True, metavar='', help='dns zone to change')
dns_parser.add_argument('--delete', action='store_true', help='delete a dns record')
dns_parser.add_argument('-k', '--api-key', metavar='', help='use the associated api key')
dns_service = dns_parser.add_mutually_exclusive_group(required=True)
dns_service.add_argument('-C', '--cloudflare', action='store_true', help='use cloudflare for domain management')
#dns_service.add_argument('-N', '--namecheap', action='store_true', help='use namecheap for domain management')
#dns_service.add_argument('-P', '--porkbun', action='store_true', help='use porkbun for domain management')
#dns_service.add_argument('-A', '--aws', action='store_true', help='use aws route 53 for domain management')
#dns_service.add_argument('-M', '--azure', action='store_true', help='use azure for domain management')

args = global_parser.parse_args()

##################################################################  END CLI PARSING ##################################################################


async def main():
    # If gaia runs on its own without args, print help
    if args.subcommand == None:
        global_parser.print_help()
        sys.exit(1)

    if args.subcommand == "install":
        import paramiko, utils.install

        # Initialize SSH
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Get connection information
        server = args.server[0].strip()
        user = args.user[0].strip()

        # Determine if we show stderr on streamed terminal output
        if args.stderr == True:
            display_stderr = True
        else:
            display_stderr = False

        # SSH port
        if args.port == True:
            port = args.port[0].strip()
        else:
            port = 22

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
            
        # Paramiko attempts SSH key auth first, then password as a fallback
        ssh.connect(hostname=server, port=port, username=user, key_filename=ssh_key, password=password, look_for_keys=True, allow_agent=True)
        
        # Update system if requested
        if args.install_updates == True:
            print("Updating remote system")
            (stdin, stdout, stderr) = ssh.exec_command("sudo apt update && sudo apt upgrade -y", get_pty=True)
            utils.install.print_terminal_output(stdout)

            if display_stderr == True:
                # Print errors so user is aware if there are any
                utils.install.print_terminal_output(stderr)


        # Install dependencies if requested
        if args.install_deps == True:
            print("Installing Dependencies")
            utils.install.convert_line_endings("install_deps.sh")
            utils.install.copy_and_execute_script(ssh=ssh, script="install_deps.sh", err=display_stderr)

        # Install Mythic and it's dependencies if true
        if args.install_mythic == True:
            print("Installing Mythic. This will take a while, so go get some coffee.")
            utils.install.convert_line_endings("install_deps.sh")
            utils.install.copy_and_execute_script(ssh=ssh, script="install_mythic.sh", err=display_stderr)

            # Get mythic admin password
            stdin, stdout, stderr = ssh.exec_command("grep 'MYTHIC_ADMIN_PASSWORD' /opt/Mythic/.env", get_pty=True)
            mythic_admin_password = stdout.readlines()
            mythic_admin_password = mythic_admin_password[0].split('"')
            mythic_admin_password = mythic_admin_password[1]

            print("Dumping mythic creds to local disk!")
            with open("mythic_admin_creds.txt", "w") as file:
                mythic_admin_creds = "mythic_admin:" + mythic_admin_password
                file.write(mythic_admin_creds)

            print("If the password for `mythic_admin` is lost, run `grep \"MYTHIC_ADMIN_PASSWORD\" /opt/Mythic/.env | cut -d \'\"\' -f 2` on the server mythic is installed on.")

        ssh.close()
        sys.exit(0)

    import utils.auth
    if args.subcommand == "auth":
        import utils.env
        
        # Authenticates to mythic if server, port, user, and password are specified
        auth_user = str(args.username[0]).strip()
        auth_password = str(args.password[0]).strip()
        mythic_host = str(args.server[0]).strip()
        mythic_port = int(args.port[0])

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

        if args.update_env == True or config == None or config["MYTHIC_API_KEY"] == '':
            # Dumps API key and mythic connection information into .env
            utils.env.update_env("MYTHIC_LOGIN_SERVER_HOST", mythic_host)
            utils.env.update_env("MYTHIC_LOGIN_SERVER_PORT", str(mythic_port))
            utils.env.update_env("MYTHIC_API_KEY", api_token)

        sys.exit(0)

    if args.subcommand == "dns":
        domain_edit = args.zone
        target_domain = args.domain
        target_value = args.value
        delete = args.delete

        # Check if the new domain record type has been set
        if args.a == None:
            print("Please specify a domain record type. Exiting!")
            sys.exit(1)
        else:
            a_record = args.a
            aaaa_record = args.aaaa
            cname_record = args.cname

        # Set record type to be passed to the function
        if a_record == True:
            record_type = "A"
        elif cname_record == True:
            record_type = "CNAME"
        elif aaaa_record == True:
            record_type = "AAAA"


        if args.cloudflare == True:
            # Validate that we have the CF API key
            import utils.dns.cf
            api_token = config["CLOUDFLARE_API_TOKEN"]

            if api_token == None:
                api_token = args.api_key

            # Get the domains listed in the account
            domains = utils.dns.cf.get_domains(api_token=api_token)
            
            # Check that our specified domain returns from this account
            for i in domains["result"]:
                if i["name"] == domain_edit:
                    domain_id = i["id"]
                    break
                else:
                    domain_id = None
                
            if domain_id == None:
                print("Please specify a valid domain. Exiting!")
                sys.exit(1)

            # Get the current dns records
            records = utils.dns.cf.get_domain_records(api_token=api_token, zone_id=domain_id)
            
            # Compare records with the intended incoming record, skip creation if it exists. Delete the record if specified.
            if records["result"] != []:
                for i in records["result"]:
                    if i["name"] == target_domain and i["type"] == record_type and i["content"] == target_value and delete != True:
                        print("Requested domain record exists in this DNS zone. Exiting!")
                        sys.exit(1)

                    elif i["name"] == target_domain and i["type"] == record_type and i["content"] == target_value and delete == True:
                        record_id = i["id"]
                        utils.dns.cf.delete_domain_record(api_token=api_token, zone_id=domain_id, dns_record_id=record_id)
                        print("Successfully deleted specified domain record.")
                        sys.exit(1)
                    
                    elif i["name"] == target_domain and delete != True:
                        print("Domain name conflicts with existing record. Please delete existing record before proceeding.")
                        sys.exit(1)
                    
                    elif delete != True:
                        record_create = utils.dns.cf.create_domain_record(api_token=api_token, zone_id=domain_id, record_name=target_domain, record_type=record_type, record_target=target_value)
                        print(record_create)
            else:
                record_create = utils.dns.cf.create_domain_record(api_token=api_token, zone_id=domain_id, record_name=target_domain, record_type=record_type, record_target=target_value)
                print(record_create)

            sys.exit(0)

    # Check if config has been changed, if not then env has not been loaded.
    if config == None:
        print("No mythic api key detected in .env. have you authenticated to mythic?")
        auth_parser.print_help()
        sys.exit(1)

    # Authenticates to mythic with API key if auth is not specified
    api_key = config["MYTHIC_API_KEY"]
    mythic_host = config["MYTHIC_LOGIN_SERVER_HOST"]
    mythic_port = config["MYTHIC_LOGIN_SERVER_PORT"]
    mythic_session = await utils.auth.mythic_login_with_api(api_token=api_key, server_host=mythic_host, server_port=mythic_port)

    # Manages users
    if args.subcommand == "users":
        import utils.users, utils.operations

        users_stdin = args.users
        stdout = args.stdout

        # Ready user list as input and prepares for merge later
        if args.user_list:
            user_list_in = args.user_list.strip()
        else:
            user_list_in = []

        # Ready user credentials list for output
        if args.user_output:
            user_list_out = args.user_output.strip()
            cred_list = []
        else:
            cred_list = None

        # Take users from stdin and list, merge, deduplicate, and prepare for passing to mythic
        users = utils.users.prepare_users(users_stdin=users_stdin, user_file_in=user_list_in)

        # Get current operations to prepare to assign a default for a new user
        operations = await utils.operations.get_operations(mythic_instance=mythic_session)
        default_operation = operations[0]
        
        # Create new users before assigning them to default operation (The first opeation that returns when getting all operations)
        if args.create == True:
            
            for i in users:
                user_creds = await utils.users.create_user(mythic_instance=mythic_session, username=i)
                await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=default_operation["name"], username=i)
                
                # Print creds if user specifies to
                if stdout == True:
                    print(user_creds)

                # Append creds to a list to prepare to dump to file if user specifies to
                if cred_list != None:
                    user_creds = user_creds + '\n'
                    cred_list.append(user_creds)

            # Dump creds to file
            if cred_list != None:
                with open(user_list_out, 'aw') as file:
                    file.writelines(cred_list)
                

        sys.exit(0)

    # Process operations
    if args.subcommand == "operations":
        import utils.operations, utils.env

        # Creates new operation
        if args.create == True:
            operation = str(args.operation[0]).strip()
            await utils.operations.create_operation(mythic_instance=mythic_session, operation_name=operation)

            # Modify env to include new operation
            if args.update_env == True or config["MYTHIC_OPERATION_NAME"] == '':
                utils.env.update_env("MYTHIC_OPERATION_NAME", operation)

        # Assign users to operations
        if args.assign == True:
            operation = args.operation
            users = args.users
            for i in operation:
                for j in users:
                    await utils.operations.add_operator_to_operation(mythic_instance=mythic_session, operation_name=i, username=j)

        sys.exit(0)

    if args.subcommand == "payloads":
        import utils.payloads, utils.env, datetime

        # Some spaghetti code incoming. If you know how to get args to play nice with a function, please tell me
        # Use specified callback url if one is supplied
        if args.callback_url:
            callback_url = args.callback_url[0].strip()
        
        # Otherwise use the value saved in env
        elif config['MYTHIC_HTTP_CALLBACK_URL_BASE'] != '' or config != None:
            callback_url = config['MYTHIC_HTTP_CALLBACK_URL_BASE']
        else:
            print("Ensure that a callback url is specified in either .env or passed via cli")
            payload_parser.print_help()
            sys.exit(1)

        # Update env file if requested or required
        if args.update_env == True or config['MYTHIC_HTTP_CALLBACK_URL_BASE'] == '':
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_URL_BASE', env_value=callback_url)

        # Callback Ports
        # Use specified callback port if one is supplied
        if args.callback_port:
            callback_port = args.callback_port[0].strip()
        
        # Otherwise use the value saved in env
        elif config['MYTHIC_HTTP_CALLBACK_PORT'] != '' or config != None:
            callback_port = config['MYTHIC_HTTP_CALLBACK_PORT']

        else:
            print("Ensure that a callback port is specified in either .env or passed via cli")
            payload_parser.print_help()
            sys.exit(1)

        # Update env file if requested or required
        if args.update_env == True or config['MYTHIC_HTTP_CALLBACK_PORT'] == '':
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_PORT', env_value=callback_port)

        # Callback Killdate
        # Use specified callback killdate if one is supplied
        if args.callback_killdate:
            callback_killdate = args.callback_killdate[0].strip()
        
        # Otherwise use the value saved in env
        elif config['MYTHIC_HTTP_CALLBACK_KILLDATE'] != '' or config != None:
            callback_killdate = config['MYTHIC_HTTP_CALLBACK_KILLDATE']
        
        # Otherwise use the default of a year
        else:
            callback_killdate_raw = datetime.date.today() + datetime.timedelta(days=365)
            callback_killdate = callback_killdate_raw.strftime("%Y-%m-%d")

        # Update env file if requested or required
        if args.update_env == True or config['MYTHIC_HTTP_CALLBACK_KILLDATE'] == '':
            utils.env.update_env(env_key='MYTHIC_HTTP_CALLBACK_KILLDATE', env_value=callback_killdate)

        # Process apollo payloads
        if args.apollo == True:
            payload_name_base = args.name[0].strip()

            # Generate normal executable
            print("Apollo portable executable building")
            payload_name_exe = payload_name_base + ".exe"
            await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="WinExe", payload_name=payload_name_exe, payload_description="Windows x64 .NET Framework Portable Executable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
            print("Apollo portable executable built")

            # Generate shellcode
            print("Apollo shellcode building")
            payload_name_bin = payload_name_base + ".bin"
            await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="Shellcode", payload_name=payload_name_bin, payload_description="Windows x64 .NET Framework Service Executable", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
            print("Apollo shellcode built")

            # Generate service executable
            print("Apollo service executable building")
            payload_name_svc = payload_name_base + "Svc.exe"
            await utils.payloads.create_apollo_payload(mythic_instance=mythic_session, output_type="Service", payload_name=payload_name_svc, payload_description="Windows x64 Shellcode", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
            print("Apollo service executable built")

            sys.exit(0)

        # process poseidon payloads
        if args.poseidon == True:
            payload_name = args.name[0].strip()
            payload_os = args.os.capitalize()


            if args.os == "linux":
                # Generate linux x64 static elf
                print("Poseidon linux x64 elf building")
                await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="AMD_x64", payload_name=payload_name, static_linking="True", payload_description="Linux x64 Static ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Poseidon linux x64 elf built")

                # Generate linux arm64 static elf
                print("Poseidon linux arm64 elf building")
                await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="ARM_x64", payload_name=payload_name, static_linking="True", payload_description="Linux arm64 Static ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Poseidon linux arm64 elf built")

            elif args.os == "macos":
                # Translates to value poseidon builder expects
                payload_os = "macOS"

                # Generate macos arm64 static elf. macOS does not like static bins for some reason.
                print("Poseidon macos x64 elf building")
                await utils.payloads.create_poseidon_payload(mythic_instance=mythic_session, os=payload_os, arch="ARM_x64", payload_name=payload_name, static_linking="False", payload_description="macOS arm64 Static ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Poseidon macos x64 elf built")
    
            else:
                print("specify os when creating poseidon payloads")
                sys.exit(0)

        # Process athena payloads
        if args.athena == True:
            payload_os = args.os.capitalize()

            if args.os == "windows":
                payload_name_base = args.name[0].strip()

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
                payload_name_base = args.name[0].strip()

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
                payload_name_base = args.name[0].strip()

                # Generate macOS arm64 .net elf
                print("Athena macos arm64 elf building")
                await utils.payloads.build_athena_payload(mythic_instance=mythic_session, os=payload_os, arch="arm64", output_type="binary", payload_name=payload_name_base, payload_description="macOS arm64 .NET ELF", http_callback_url=callback_url, http_callback_port=callback_port, http_callback_killdate=callback_killdate)
                print("Athena macos arm64 elf built")

            else:
                print("specify os when creating athena payloads")
                sys.exit(0)

        sys.exit(0)


if __name__ == '__main__':
     asyncio.run(main())

sys.exit(0)