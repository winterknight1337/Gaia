# Usage Instructions
1. Install the `mythic` package from pip (I highly recommend a virtual environemnt).
2. Create a file called `users.txt` with the usernames you would like to provision.
3. Run install.sh as root on a debian, kali, or ubuntu box and it should Just Work™️!
4. User credentials will be created in a file called `users.txt`.

# Acknowledgements
[@its-a-feature](https://github.com/its-a-feature) for creating Mythic and the docker install scripts this project uses.

# TODO
- [ ] Figure out webhooks
- [ ] Pre-compile the following
    - [ ] Apollo (Windows) executable
    - [ ] Apollo (Windows) shellcode
    - [ ] Poseidon (Linux and macOS) executable
- [x] Figure out some sort of automated user provisioning?
- [ ] Work on a defender-bypassing Apollo shellcode loader (separate repo)
