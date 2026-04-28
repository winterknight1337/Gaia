#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root";
  exit;
fi

echo "Installing prerequisites!";
apt install git vim make -y;

echo "Installing Docker!";

OS=$(cat /etc/os-release | grep "^ID=" | cut -d "=" -f 2);

if [ $OS == "debian" ] 
    then wget https://raw.githubusercontent.com/its-a-feature/Mythic/refs/heads/master/install_docker_debian.sh;
    chmod 770 install_docker_debian.sh;
    source ./install_docker_debian.sh;
    echo "Docker install completed";
    rm ./install_docker_debian.sh;

elif [ $OS == "kali" ]
    then wget https://github.com/its-a-feature/Mythic/raw/refs/heads/master/install_docker_kali.sh;
    chmod 770 install_docker_kali.sh;
    source ./install_docker_kali.sh;
    echo "Docker install completed";
    rm ./install_docker_kali.sh;

elif [ $OS == "ubuntu" ]
    then wget https://github.com/its-a-feature/Mythic/raw/refs/heads/master/install_docker_ubuntu.sh;
    chmod 770 install_docker_ubuntu.sh;
    source ./install_docker_ubuntu.sh;
    echo "Docker install completed";
    rm ./install_docker_ubuntu.sh;

else
    echo "[-] Please run on debian, kali, or ubuntu.";
    exit -1;
fi
echo "Cleaning up Docker install script";
exit 0;