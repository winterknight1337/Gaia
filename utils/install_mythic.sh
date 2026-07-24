#!/usr/bin/bash

# Root check
if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root";
  exit;
fi
echo "****Preparing to install Mythic! Standby!****";

# Download, build, and Install Mythic components
cd /opt/;

echo "Pulling Mythic Repo";
git clone https://github.com/its-a-feature/Mythic.git --depth 1;
cd Mythic;

echo "Building mythic-cli binary";
make;

echo "Booting Mythic up for the first time!";
$PWD/mythic-cli start;

echo "Installing Apollo (Windows Agent)!";
$PWD/mythic-cli install github https://github.com/MythicAgents/Apollo.git --force;

echo "Installing Poseidon (POSIX Agent)!";
$PWD/mythic-cli install github https://github.com/MythicAgents/poseidon.git --force;

echo "Installing Athena (Cross-Platform Agent)";
$PWD/mythic-cli install github https://github.com/MythicAgents/Athena.git --force;

echo "Installing http C2 profile!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/http.git --force;

echo "Installing smb C2 profile!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/smb.git --force;

echo "Installing Forge!";
$PWD/mythic-cli install github https://github.com/MythicAgents/forge.git --force;

echo "Installing Webhooks!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/basic_webhook.git --force;

echo "Installing Registry Browser!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/registry_browser.git --force;

echo "Installing LDAP Browser!";
$PWD/mythic-cli install github https://github.com/MythicC2Profiles/ldap_browser.git --force;

echo "Mythic webserver hosted and ready via HTTPS on port 7443!";
admin_passwd=$(grep "MYTHIC_ADMIN_PASSWORD" /opt/Mythic/.env | cut -d '"' -f 2)
echo "Use mythic_admin:$admin_passwd to connect to the C2 server!";

echo "Dumping mythic_admin creds to creds.txt";
echo "mythic_admin:$admin_passwd" > $SUDO_HOME/creds.txt;
exit 0;
