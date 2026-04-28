#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root";
  exit;
fi
echo "****Preparing to install Mythic Prerequisites!****"

echo "Performing apt update and upgrade!"
apt update && apt upgrade -y;

exit 0;