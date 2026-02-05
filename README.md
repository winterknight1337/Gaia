# Usage Instructions
1. Create a and activate a python venv 
2. Install requisite packages `pip install -r requirements.txt`
3. Run `install.sh` as root on a debian, kali, or ubuntu box. It will install Mythic and create a default admin account on the box that executes `install.sh`
4. Copy `.env-template` to `.env`
5. Populate the values of `.env` with values of your choosing
6. Execute the script that executes your desired set of actions

# Acknowledgements
[@its-a-feature](https://github.com/its-a-feature) for creating Mythic, the docker install scripts this project uses (that I shamelessly stole from the [Mythic repo](https://github.com/its-a-feature/Mythic)), and the jupyter notebooks that I based most of these scripts on.
[@BlaiseOfGlory](https://github.com/BlaiseOfGlory) for pointing me to some resources to get this project off the ground. 

# TODO
- [x] Script out operation creation
- [x] Figure out webhooks
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
