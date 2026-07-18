import os

def copy_and_execute_script(ssh, script: str, err: bool=False):
    # Open SFTP Channel to copy script
    sftp = ssh.open_sftp()

    # Get the base directory for the project and add install_deps.
    # Required since paramiko's implementation of SFTP is not shell aware
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, f"{script}")

    # Get the home directory and place the script in it before closing
    (stdin, stdout, stderr) = ssh.exec_command('echo $HOME')
    home_dir = stdout.read().decode().strip()
    sftp.put(localpath=local_path, remotepath=f"{home_dir}/{script}")
    sftp.close()

    # Execute depednency install script
    ssh.exec_command(f"chmod 770 ~/{script}", get_pty=True)
    (stdin, stdout, stderr) = ssh.exec_command(f"sudo bash ~/{script}", get_pty=True)

    print_terminal_output(stdout)

    if err == True:
        print("stderr output:")
        print_terminal_output(stderr)

    # Removing shell script
    print(f"Cleaning up {script} script")
    ssh.exec_command(f"rm {script}")

def print_terminal_output(channel):
    for line in iter(channel.readline, ""):
        print(line, end="")

def convert_line_endings(script: str):
    # Get the base directory for the project and add install_deps.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, f"{script}")

    with open(local_path, "r") as file:
        contents = file.read()
    
    with open(local_path, "w", newline="\n") as file:
        file.write(contents)

def copy_file(ssh, file: str, err: bool = False):
    # Open SFTP Channel to copy script
    sftp = ssh.open_sftp()

    # Get the base directory for the project and add install_deps.
    # Required since paramiko's implementation of SFTP is not shell aware
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, f"../{file}")

    # Get the home directory and place the script in it before closing
    (stdin, stdout, stderr) = ssh.exec_command('echo $HOME')
    home_dir = stdout.read().decode().strip()
    sftp.put(localpath=local_path, remotepath=f"{home_dir}/{file}")
    sftp.close()

def copy_gaia_ssh_key(ssh, err: bool = False):
    # Open SFTP Channel to copy script
    sftp = ssh.open_sftp()

    home_dir = os.path.expanduser("~")
    ssh_key = f"{home_dir}/.ssh/gaia-redir.pem"

    # Get the home directory and place the script in it before closing
    (stdin, stdout, stderr) = ssh.exec_command('echo $HOME')
    home_dir = stdout.read().decode().strip()
    sftp.put(localpath=ssh_key, remotepath=f"{home_dir}/.ssh/gaia-redir.pem")
    sftp.close()