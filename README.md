# Description
Gaia is a tool designed to manage a Mythic C2 installation with an emphasis on learning and lab usage. This emphasis is enforced by its usage of non-evasive payloads and Mythic C2 profiles. Gaia streamlines server standup to create a solid foundation of bundled tools and deafults to make Mythic easy to use for training.

Quick note, this is more of a reference-style document. If you are looking for something more of a usage guide, click [here](./COMPLETE.md).

It supports the following capabilities:
- Installation of the following components
    - [Apollo](https://github.com/MythicAgents/Apollo)
    - [Poseidon](https://github.com/MythicAgents/poseidon)
    - [Athena](https://github.com/MythicAgents/Athena)
    - [Forge](https://github.com/MythicAgents/forge)
    - [http C2 profile](https://github.com/MythicC2Profiles/http)
    - [SMB C2 profile](https://github.com/MythicC2Profiles/smb)
    - [LDAP Browser](https://github.com/MythicC2Profiles/ldap_browser)
    - [Registry Browser](https://github.com/MythicC2Profiles/registry_browser)
    - [Webhooks](https://github.com/MythicC2Profiles/basic_webhook)
- Operation creation and user assignment
- User creation
- Payload creation
- Redirector creation and management
- Domain management

# Prerequisites
## Core Prerequisites
1. Debian, Kali, or Ubuntu server or VM
    - If the system is a VM, I recommend at least 2 cores and 4GB of RAM, but prefer 4 cores and 8GB of RAM
    - The system must be configured to allow either:
        - SSH into `root` account
        - SSH into another account configured to allow `sudo` without a password

2. Create Python venv
    - Linux
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    - Windows
        ```powershell
        python3.exe -m venv .venv
        Scripts/Activate.ps1
        ```

3. Install required packages
    ```bash
    pip3 install -r requirements.txt
    ```

## Optional Pre-requisites
These are used if you wish to create redirectors in AWS.
### AWS account scoped to modification of EC2 resources
This can technically be the root account, however I would recommend creating another Gaia specific user with MFA and group in IAM to accomplish this.
The IAM account needs the following rights assigned in IAM Policies
- `ec2:RunInstances`
- `ec2:DescribeInstances`
- `ec2:TerminateInstances`
- `ec2:DescribeLaunchTemplates`
- `ec2:DescribeLaunchTemplateVersions`
- `ec2:StopInstances`
- `ec2:DescribeSecurityGroups`
- `ec2:DescribeImages`
- `ec2:GetLaunchTemplateData`
- `ec2:DescribeNetworkInterfaces`
- `ec2:StartInstances`
- `ec2:DescribeAvailabilityZones`
- `ec2:DescribeVpcs`
- `ec2:DescribeVolumes`
- `ec2:DescribeSubnets`
- `ec2:DescribeKeyPairs`
- `ec2:CreateKeyPair`
- `ec2:CreateSecurityGroup`
- `ec2:CreateTags`
- `ec2:AuthorizeSecurityGroupIngress`
- `ec2:DeleteKeyPair`
- `ec2:DeleteSecurityGroup`

### Access Keys for given AWS account
Access keys for IAM users can be created in IAM on the user page. You will need both the access and secret access keys so Gaia can connect to you AWS account and modify resources over the API.

### Cloudflare or PorkBun account with API keys
Finally, if you wish to manage DNS through Gaia, you'll need API keys for either Cloudflare or Porkbun.

# Usage Instructions
Basic Usage of Gaia
```bash
./gaia -h
usage: gaia [-h] [-v] {install,auth,operation,user,payload,dns,redirector} ...

Lightweight helper tool to install and manage Mythic c2 with a focus on students, CTF players, Mythic developers, and security researchers

options:
  -h, --help                                            show this help message and exit
  -v, --version                                         Display software version

Modules:
  {install,auth,operation,user,payload,dns,redirector}
    install                                             Installs Mythic on Debian, Ubuntu, or Kali
    auth                                                Authenticate to Mythic
    operation                                           Manage operations in Mythic
    user                                                Manage users in Mythic
    payload                                             Manage payloads in Mythic
    dns                                                 Manage DNS records with 3rd party registrars
    redirector                                          Manage redirector configuration within public clouds
```

### Gaia Install
Gaia install help
```bash
./gaia.py install -h
usage: gaia install [-h] [--install-updates] [--install-deps] [--install-mythic] -S  [-P 22] -u  [-p ] [-i path/to/file] [--stderr] [-k]

options:
  -h, --help                        show this help message and exit
  --install-updates                 Update target server with apt before installing Mythic
  --install-deps                    Install dependencies required for Mythic on target server
  --install-mythic                  Install Mythic on target server
  -S, --server                      Hostname or IP address of target server
  -P, --port 22                     SSH port of target server
  -u, --user                        User to authenticate as over SSH on target server
  -p, --password                    SSH user password or SSH key passphrase
  -i, --identity-file path/to/file  SSH key for authentication
  --stderr                          Show stderr from install steps from target server after stdout
  -k, --no-ssl                      Don't verify TLS certificates when authenticating to Mythic
```

Mythic and depedency installation example with Gaia.
```bash
./gaia.py install -S 192.168.1.1 -u winterknight --install-updates --install-deps --install-mythic
```
The above example assumes a relatively common SSH private key name that paramiko can find on it's own. For example, `id_rsa` or `id_ed25519`. Custom SSH key names can be defined with `-i` and either a relative or absolute path. Additionally, if the SSH key has a passphrase, that can be captured with `-p` and used with the SSH key.

### Gaia Auth
Gaia auth help
```bash
./gaia.py auth -h
usage: gaia auth [-h] -S  -P 7443 -u mythic_admin -p

options:
  -h, --help               show this help message and exit
  -S, --server             Hostname or IP address of Mythic server
  -P, --port 7443          Port to access Mythic's web interface
  -u, --user mythic_admin  Target user for Mythic authentication
  -p, --password           Password for target user for Mythic authentication
```

Authenticates to Mythic and dumps the API key to `.env`.
```bash
./gaia.py auth -S 192.168.1.1 -u mythic_admin -p
```

### Gaia Operation
Gaia operation help
```bash
./gaia.py auth --help           
usage: gaia auth [-h] -S  -P 7443 -u mythic_admin -p

options:
  -h, --help               show this help message and exit
  -S, --server             Hostname or IP address of Mythic server
  -P, --port 7443          Port to access Mythic's web interface
  -u, --user mythic_admin  Target user for Mythic authentication
  -p, --password           Password for target user for Mythic authentication
```

List current Mythic operations with Gaia.
```bash
./gaia.py operation list
```

Create a new Mythic operation with Gaia and assign specified users to it.
```bash
./gaia.py operation create -n mwccdc -u WinterKnight, RedefiningReality, Grafftix
```

Assign users to an operation in Mythic.
```bash
./gaia.py operation assign -o mwccdc -u WinterKnight, tal0n, AGrapplerNamedSam
```

### Gaia User
Create new users in Mythic with Gaia from a user list and dump new creds to disk.
```bash
./gaia.py user create -l ./users.txt -d ./creds.txt
```

Use Gaia to create new Mythic users with usernames specified on CLI and creds printed to stdout.
```bash
./gaia.py user create -u WinterKnight, elrey, Armada, ilree --stdout
```

### Gaia Payload
Listing current payloads in Mythic with Gaia.
```bash
./gaia.py payload list
```

Payload creation help
```bash
./gaia.py payload create -h
usage: gaia payload create [-h] {apollo,poseidon,athena} ...

Create new payloads

options:
  -h, --help                show this help message and exit

Agents:
  {apollo,poseidon,athena}  Create a payload from the specified agent
    apollo                  Manage Apollo payloads
    poseidon                Manage Poseidon payloads
    athena                  Manage Athena payloads
```

Creating Poseidon payloads without a redirector for your local network (For lab, dev, and research usage).
```bash
./gaia.py payload create poseidon -n notmalware -u http://192.168.1.1 -p 80 -os linux
```

Creating Poseidon payloads without a redirector for your local network (For lab, dev, and research usage).
```bash
./gaia.py payload create athena -n dotnet_cross -u http://192.168.1.1 -p 80 -os macos
```

Creating Apollo payloads through a redirector with a killdate (For CCDC or other sanctioned remote targets).
```bash
./gaia.py payload create apollo -n notapollo -u https://mythic.example.com -p 443 -k 2026-08-09
```

### Gaia DNS
Gaia supports 2 dns providers at this time. Cloudflare and Porkbun. Additional providers are being considered for future versions of Gaia. If you have any requests, please let me know!
Gaia currently supports DNS record creation, deletion, and listing. As of now Gaia assumes that there is a single foreward lookup zone on the domain which you intend to use for C2. I *highly recommend* utilizing a throwaway C2 for this purpose, as evidence of C2 traffic going through a legitimate domain is subject to significant scrutiny from security and domain reputation vendors.

#### Gaia DNS Through Cloudflare
Cloudflare domain record creation help
```bash
./gaia.py dns cloudflare create -h
usage: gaia dns cloudflare create [-h] [-k] [-d ] [-n ] [-v ] [-t {a,aaaa,cname}]

options:
  -h, --help                        show this help message and exit
  -k, --api-key                     Enter Cloudflare API token when requested
  -d, --domain                      Creates new records in target domain
  -n, --record-name                 Name of new domain record
  -v, --record-value                Value of domain record: IP address for A or AAAA record, or FQDN for CNAME alias
  -t, --record-type {a,aaaa,cname}  Type of domain record to create
```

Listing current domains available in Cloudflare with API key request
```bash
./gaia.py dns cloudflare list -k
```

Creating a new A record in Cloudflare
```bash
./gaia.py dns cloudflare create -d example.com -n mythic -t a -v 1.1.1.1 
```

Cloudflare domain record deletion help
```bash
./gaia.py dns cloudflare delete -h
usage: gaia dns cloudflare delete [-h] [-k] [-d ] [-n ]

options:
  -h, --help          show this help message and exit
  -k, --api-key       Enter Cloudflare API token when requested
  -d, --domain        Deletes records from target domain
  -n, --record-name   Name of domain record to delete
```

Deleting a domain record in Cloudflare
```bash
./gaia.py dns cloudflare delete -d exmaple.com -n www
```

### Gaia DNS through Porkbun
Listing current domains wtih Porkbun with API keys requested
```bash
./gaia dns porkbun list -k -s
```

Porkbun domain record creation help
```bash
./gaia.py dns porkbun create -h
usage: gaia dns porkbun create [-h] [-k] [-s] [-d ] [-n ] [-v ] [-t {a,aaaa,cname}]

options:
  -h, --help                        show this help message and exit
  -k, --api-key                     Enter the Porkbun API key when requested
  -s, --secret-key                  Enter the Porkbun secret key when requested
  -d, --domain                      Creates new records in target domain
  -n, --record-name                 Name of new domain record
  -v, --record-value                Value of domain record: IP address for A or AAAA record, or FQDN for CNAME alias
  -t, --record-type {a,aaaa,cname}  Type of domain record to create
```

Porkbun domain record creation
```bash
./gaia.py dns porkbun create -d example.com -n test -t cname -v www.example.com
```

Porkbun domain record deletion help
```bash
./gaia.py dns porkbun delete -h
usage: gaia dns porkbun delete [-h] [-k] [-s] [-d ] [-n ]

options:
  -h, --help          show this help message and exit
  -k, --api-key       Enter the Porkbun API key when requested
  -s, --secret-key    Enter the Porkbun secret key when requested
  -d, --domain        Deletes records from target domain
  -n, --record-name   Name of domain record to delete
```

Porkbun domain record deletion
```bash
./gaia.py dns porkbun delete -d example.com -n test
```

### Gaia Redirector
This is the area that I expect students to struggle with the most. I will be writing an Intro to C2s blog post in the future, which I will link here when it's written. 

Gaia redirector help
```bash
./gaia.py redirector -h
usage: gaia redirector [-h] {create,delete,certbot,generate,tunnel} ...

options:
  -h, --help                               show this help message and exit

Redirector Actions:
  Manage redirectors

  {create,delete,certbot,generate,tunnel}
    create                                 Create a new redirector
    delete                                 Delete a redirector
    certbot                                Install Certbot and enable HTTPS on a redirector
    generate                               Generate redirector rules based on existing payload in Mythic and upload them to redirector
    tunnel                                 Configure SSH tunnel between Mythic server and redirector
```

Currently redirectors can only be created in AWS. Future versions of Gaia will include the ability to create redirectors in Azure as well.
AWS Redirector creation help
```bash
./gaia.py redirector create aws -h     
usage: gaia redirector create aws [-h] [-a] [-s] -S {t2.micro,t2.small,t2,medium,t3.micro,t3.small,t3.medium} [-r REGION] -o {debian,ubuntu}
                                                                                                                                         
options:                                                                                               
  -h, --help                                                            show this help message and exit
  -a, --access-key                                                      Enter the AWS access key when requested
  -s, --secret-key                                                      Enter the AWS secret key when requested
  -S, --size {t2.micro,t2.small,t2,medium,t3.micro,t3.small,t3.medium}  Size of redirector EC2
  -r, --region REGION                                                   Create redirector in target AWS region
  -o, --os {debian,ubuntu}                                              Specify OS for the redirector
```

Creating a redirector in AWS
```bash
./gaia.py redirector create aws -r us-east-2 -S t3.micro -o debian -a -s
```

Deleting a redirector in AWS
```bash
./gaia.py redirector delete aws
```

When Gaia creates infrastructure in AWS, it tags it with `createdBy:gaia`. The AWS redirector deletion functionality searches for, and deletes EC2 instances, keypairs, and security groups with this tag.

Redirector certbot help
```bash
./gaia.py redirector certbot -h    
usage: gaia redirector certbot [-h] -d  -S  -u  [-P ] [-i path/to/file] [--stderr]

options:
  -h, --help                        show this help message and exit
  -d, --domain                      FQDN for target website to request TLS certificates
  -S, --redirector-server           Hostname or IP address of target server to execute certbot
  -u, --redirector-user             User to authenticate as over SSH on target server
  -P, --password                    SSH user password or SSH key passphrase
  -i, --identity-file path/to/file  SSH key for authentication
  --stderr                          Show stderr from install steps from target server after stdout
```

Creating a TLS certificate with Certbot
```bash
./gaia.py redirector certbot -d mythic.example.com -S 1.1.1.1 -u admin -i ~/.ssh/gaia.key.pem
```

Redirector generate help
```bash
./baia.py redirector generate -h
usage: gaia redirector generate [-h] -u  -t  -rS  -ru  [-rp ] [-ri path/to/file]

options:
  -h, --help                                   show this help message and exit
  -u, --payload-uuid                           UUID of payload to use as the basis of apache mod_rewrite rule generation
  -t, --redirect-target                        URL of website to redirect non-c2 traffic to
  -rS, --redir-server                          Hostname or IP address of redirector server
  -ru, --redir-ssh-user                        User to authenticate as over SSH on redirector server
  -rp, --redir-ssh-password                    Redirector SSH user password or SSH key passphrase
  -ri, --redir-ssh-identity-file path/to/file  SSH key for authentication
```

.htaccess file generation example
```bash
./gaia.py -u 266f58c3-0fdf-4d15-87e8-12b65d7d990c -t www.example.com -rS mythic.example.com -ru admin -ri ~/.ssh/gaia-redir.pem
```

Gaia redirector tunnel help
```bash
./gaia.py redirector tunnel -h
usage: gaia redirector tunnel [-h] -mS  [-mP ] -mu  [-mp ] [-mi path/to/file] -rS  -ru 

options:
  -h, --help                                    show this help message and exit
  -mS, --mythic-server                          Hostname or IP address of Mythic server
  -mP, --mythic-ssh-port                        SSH port for Mythic server
  -mu, --mythic-ssh-user                        User to authenticate as over SSH on redirector server
  -mp, --mythic-ssh-password                    Mythic SSH user password or SSH key passphrase
  -mi, --mythic-ssh-identity-file path/to/file  SSH key for authentication
  -rS, --redir-server                           Hostname or IP address of redirector server
  -ru, --redir-ssh-user                         User to authenticate as over SSH on redirector server
```

Creating SSH tunnel between Mythic server and redirector
```bash
./gaia.py redirector tunnel -ms 192.168.1.1 -mu WinterKnight -rS mythic.example.com -ru admin
```
Note the above command will automatically look for `gaia-redir.pem` that gets created and dumped to the user's `.ssh` folder when spinning up redirectors in AWS.

# Some notes on .env
Some items in this tool uses a `.env` file. You may either pre-fill the values by copying `.env-template` to `.env` and manually filling them in, or you may specify them in the CLI and Gaia will populate it into the relevant section automatically. The idea here was to prevent the need to endlessly copy-paste some of the more tedious parts of the CLI like API keys. The variables placed in `.env` should rarely change. The names given in `.env` will either closely or exactly match the value given on the CLI. 


# Acknowledgements
I want to give a shout out to [@its-a-feature](https://github.com/its-a-feature) for his work creating and mainting Mythic and it's libraries that I use in this project.
I'd like to give another shout out to [@BlaiseOfGlory](https://github.com/BlaiseOfGlory) for giving me some tips on where to start on this project.
[@AGrapplerNamedSam](https://github.com/AGrapplerNamedSam) and [elreydetoda](https://github.com/elreydetoda) for helping me test pre-release versions of Gaia. Having both a Specter's and a student's perspective on this was extremely helpful!
Last but not least @leidy-tector and the greater SpecterOps team for enabling and encouraging me to work on this!