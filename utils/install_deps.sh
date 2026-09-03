#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root";
  exit;
fi

echo "#########################";
echo "# Updating apt sources! #";
echo "#########################";
apt update;

echo "#############################";
echo "# Installing prerequisites! #";
echo "#############################";
apt install git vim make autossh -y;

echo "######################";
echo "# Installing Docker! #";
echo "######################";

OS=$(cat /etc/os-release | grep "^ID=" | cut -d "=" -f 2);
VERSION_ID=$(cat /etc/os-release | grep "^VERSION_ID=" | cut -d "=" -f 2 | cut -d '"' -f 2);

if [ $OS == "debian" ] && [ $VERSION_ID == "12" ]
    then echo '[+] Installing Docker for Debian 12';
    wget https://raw.githubusercontent.com/its-a-feature/Mythic/refs/heads/master/install_docker_debian.sh;
    chmod 770 install_docker_debian.sh;
    source ./install_docker_debian.sh;
    echo '[+] Cleaning up Docker install script';
    rm ./install_docker_debian.sh;

elif [ $OS == "debian" ] && [ $VERSION_ID == "13" ]
    then echo '[+] Installing Docker for Debian 13'
    apt install -y apt-transport-https ca-certificates curl gnupg2;
    install -m 0755 -d /etc/apt/keyrings;
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc;
    chmod a+r /etc/apt/keyrings/docker.asc;
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list;
    apt update;
    apt-get install -y --no-install-recommends docker-ce docker-compose-plugin;
    echo '[+] Cleaning up Docker install script';
    rm ./install_docker_debian.sh

elif [ $OS == "kali" ]
    then echo '[+] Installing Docker for Kali'
    then wget https://github.com/its-a-feature/Mythic/raw/refs/heads/master/install_docker_kali.sh;
    chmod 770 install_docker_kali.sh;
    source ./install_docker_kali.sh;
    echo '[+] Cleaning up Docker install script';
    rm ./install_docker_kali.sh;

elif [ $OS == "ubuntu" ]
    then echo '[+] Installing Docker for Ubuntu'
    then wget https://github.com/its-a-feature/Mythic/raw/refs/heads/master/install_docker_ubuntu.sh;
    chmod 770 install_docker_ubuntu.sh;
    source ./install_docker_ubuntu.sh;
    echo '[+] Cleaning up Docker install script';
    rm ./install_docker_ubuntu.sh;

else
    echo "[-] Please run on debian, kali, or ubuntu.";
    exit -1;
fi
echo '[+] Docker install completed!';
exit 0;
