# Description
Gaia is a tool designed to manage a Mythic C2 installation with an emphasis on learning and lab usage. This emphasis is enforced by its usage of non-evasive payloads and Mythic C2 profiles. Gaia streamlines server standup to create a solid foundation of bundled tools and deafults to make Mythic easy to use for training.

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
- Operation management
- User creation and operation assignment
- Payload creation

# Prerequisites
1. Debian, Kali, or Ubuntu server configured to allow either:
    - SSH into `root` account
    - SSH account configured to allow `sudo` without a password

2. Create Python venv
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install required packages
    ```bash
    pip3 install -r requirements.txt
    ```

# Usage Instructions
Use Gaia to install Mythic on a remote system over over SSH using a password.
```bash
python3 gaia.py install -S <remote_host> -p <port> -u <username> -p <password> -D -M
```

Use Gaia to install Mythic on a remote system over over SSH using an SSH key. If both password and SSH key are supplied the SSH key takes precedent.
```bash
python3 gaia.py install -S <remote_host> -p <port> -u <username> -i <path/to/ssh_key> -D -M
```
Feel free to get some coffee, it will be a little while until everything is completed.


To authenticate to Mythic once it's installed
```bash
python3 gaia.py auth -S <mythic_host> -P <mythic_interface_port> -u mythic_admin -p '<random_gen_password>
```


To create new users for Mythic passing users with stdin and new creds with stdout
```bash
python3 gaia.py users -i winterknight, test, test2 -s -c
```


To create new users for Mythic passing users in with a file and new creds to a file
```bash
python3 gaia.py users -l /path/to/file -o /path/to/file -c
```


To create a new operation in Mythic and assign a mythic user to it
```bash
python3 gaia.py operations -o <operation_name> -c -u winterknight -a
```


To create new Apollo payloads
```bash
python3 gaia.py payloads --apollo -n apollo -U https://192.168.1.1 -P 443 -K 2026-05-10
```


To create new Poseidon payloads
```bash
python3 gaia.py payloads --poseidon -n poseidon -U https://192.168.1.1 -P 443 -K 2026-05-10 -o linux
```


To create new Athena payloads
```bash
python3 gaia.py payloads --athena -n athena -U https://192.168.1.1 -P 443 -K 2026-05-10 -o macos
```

# Acknowledgements
I want to give a shout out to [@its-a-feature](https://github.com/its-a-feature) for his work creating and mainting Mythic, and it's python libraries I use in this project. I'd like to give another shout out to [@BlaiseOfGlory](https://github.com/BlaiseOfGlory) for giving me some tips on where to start on this project @AGrapplerNamedSam for helping me test, and last but not least @leidy-tector for enabling and encouraging me to work on this!