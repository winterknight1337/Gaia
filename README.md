# Usage Instructions
1. Install the `mythic` package from pip (I highly recommend a virtual environemnt)
2. Create a file called `users.txt` with the usernames you would like to provision
3. Run install.sh as root on a debian, kali, or ubuntu box. It will install Mythic and create a default admin account
4. User credentials will be created in a file called `users.txt`
5. Populate the global variables of `create_users.py` with those applicable to your mythic install
6. Run create_users.py with python
7. Run create_payloads.py with python

# Acknowledgements
[@its-a-feature](https://github.com/its-a-feature) for creating Mythic, the docker install scripts this project uses (that I shamelessly stole from the Mythic repo), and the jupyter notebooks that I based most of these scripts on.

# TODO
- [x] Script out operation creation
- [ ] Figure out webhooks
- [x] Pre-compile the following
    - [x] Apollo (Windows) Windows PE executable
    - [x] Apollo (Windows) Windows Service executable
    - [x] Apollo (Windows) shellcode
    - [x] Poseidon (Linux x86) executables
    - [x] Poseidon (Linux ARM) executables
    - [x] Poseidon (MacOS ARM) executables
    - [x] Athena payloads
- [x] Figure out some sort of automated user provisioning?
- [ ] Major refactor to clean this mess up
    - [ ] Work on a real CLI
- [ ] Work on a defender-bypassing Apollo shellcode loader (separate repo)
