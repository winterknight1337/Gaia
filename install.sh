#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root";
  exit;
fi
echo "****Preparing to install Mythic Standby!****"

echo "Performing apt update and upgrade!"
apt update && apt upgrade -y;

echo "Installing prerequisites!";
apt install git vim make -y;

# Download and build Mythic
# Consider implementing detection for number of CPUs and RAM
# Make echos from this script more noticable
echo "Pulling Mythic Repo"
cd /opt/;
git clone https://github.com/its-a-feature/Mythic.git --depth 1;
cd Mythic;

echo "Installing docker";

OS=$(cat /etc/os-release | grep "^ID=" | cut -d "=" -f 2);

if [ $OS == "debian" ] 
    then $PWD/install_docker_debian.sh;
    rm install_docker_debian.sh;
    
elif [ $OS == "kali" ]
    then $PWD/install_docker_kali.sh;
    rm install_docker_kali.sh;

elif [ $OS == "ubuntu" ]
    then $PWD/install_docker_ubuntu.sh;
    rm install_docker_ubuntu.sh;

else
    echo "[-] Please run on debian, kali, or ubuntu.";
    exit -1;
fi

echo "Building mythic-cli binary";
make;

echo "Booting Mythic up for the first time!";
$PWD/mythic-cli start;

echo "Installing Apollo (Windows Agent)!";
$PWD/mythic-cli install github https://github.com/MythicAgents/Apollo.git;

echo "Installing Poseidon (Linux Agent)!";
$PWD/mythic-cli install github https://github.com/MythicAgents/poseidon.git;

echo "Installing Athena (Cross-Platform Agent)";
$PWD/mythic-cli install github https://github.com/MythicAgents/Athena.git;

echo "Installing http C2 profile!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/http.git;

echo "Installing smb C2 profile!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/smb.git;

echo "Installing Forge!";
sudo $PWD/mythic-cli install github https://github.com/MythicAgents/forge.git;

echo "Mythic webserver hosted and ready via HTTPS on port 7443!";
admin_passwd=$(grep "MYTHIC_ADMIN_PASSWORD" /opt/Mythic/.env | cut -d '"' -f 2)
echo "Use mythic_admin:$admin_passwd to connect to the C2 server!";

echo "Dumping mythic_admin creds to creds.txt";
echo "mythic_admin:$admin_password" > $PWD/creds.txt;
exit 0;