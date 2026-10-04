import sys, utils.redirector.generic, utils.env
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network.models import VirtualNetwork, AddressSpace, Subnet, NetworkSecurityGroup, SecurityRule, PublicIPAddress, NetworkInterface, NetworkInterfaceIPConfiguration
from azure.mgmt.compute.models import VirtualMachine, HardwareProfile, StorageProfile, ImageReference, OSProfile, LinuxConfiguration, SshPublicKey, SshConfiguration, NetworkInterfaceReference, OSDisk, NetworkProfile
from prettytable import PrettyTable

def create_resource_group(az_resource_auth: ResourceManagementClient, region: str):
    az_resource_auth.resource_groups.create_or_update(
        resource_group_name = "Gaia",
        parameters= {
            "location" : region,
            "tags" : {
                "createdBy" : "Gaia"
            }
        }
    )

def create_network(az_network_auth: NetworkManagementClient, region: str, address_prefix: str):
    response = az_network_auth.virtual_networks.begin_create_or_update(
        resource_group_name = "Gaia",
        virtual_network_name = "Gaia-vNet",
        parameters = VirtualNetwork(
            location = region,
                address_space = AddressSpace(
                    address_prefixes = [address_prefix]
            ),
            subnets = [
                Subnet(
                    name = "Gaia",
                    address_prefix = address_prefix,
                )
            ],
            tags = {
                "createdBy" : "Gaia"
            },
        ),
    ).result()

    return response

def create_network_security_group(az_network_auth: NetworkManagementClient, region: str):
    response = az_network_auth.network_security_groups.begin_create_or_update(
        resource_group_name = "Gaia",
        network_security_group_name = "Gaia-NSG",
        parameters = NetworkSecurityGroup(
            location = region,
            tags = {
                "createdBy" : "Gaia"
            },
        ),
    ).result()

    return response

def create_network_security_group_rule(az_network_auth: NetworkManagementClient, rule_name: str, rule_port:str, rule_priority: str):
    response = az_network_auth.security_rules.begin_create_or_update(
        resource_group_name = "Gaia",
        network_security_group_name = "Gaia-NSG",
        security_rule_name = rule_name,
        security_rule_parameters = SecurityRule(
            protocol = "Tcp",
            source_address_prefix = "*",
            source_port_range = "*",
            destination_address_prefix = "*",
            destination_port_range = rule_port,
            access = "Allow",
            direction = "Inbound",
            priority = rule_priority
        ),
    ).result()

    return response

def create_public_ip_address(az_network_auth: NetworkManagementClient, region: str):
    response = az_network_auth.public_ip_addresses.begin_create_or_update(
        resource_group_name = "Gaia",
        public_ip_address_name= "Gaia-Redir-IP",
        parameters = PublicIPAddress(
            location = region,
            sku = {
                "name" : "Standard"
            },
            public_ip_allocation_method = "Static",
            public_ip_address_version = "IPv4",
            tags = {
                "createdBy" : "Gaia"
            }
        ),
    ).result()

    return response

def create_network_interface(az_network_auth: NetworkManagementClient, region: str, subnet_id: str, ip_id:str, nsg_id:str):
    response = az_network_auth.network_interfaces.begin_create_or_update(
        resource_group_name = "Gaia",
        network_interface_name = "Gaia-Redir-NIC",
        parameters = NetworkInterface(
            location = region,
            ip_configurations = [
                NetworkInterfaceIPConfiguration(
                    name = "Gaia",
                    subnet = {
                        "id" : subnet_id
                    },
                    public_ip_address = {
                        "id" : ip_id
                    }
                )
            ],
            tags = {
                "createdBy" : "Gaia"
            },
            network_security_group = NetworkSecurityGroup(
                id = nsg_id
            ),
        )
    ).result()

    return response

def create_ssh_key_object(az_compute_auth: ComputeManagementClient, region:str):
    response = az_compute_auth.ssh_public_keys.create(
        resource_group_name = "Gaia",
        ssh_public_key_name = "gaia-redir",
        parameters = {
            "location" : region,
            "tags" : {
                "createdBy" : "Gaia"
            },
        }
    )

    return response

def generate_ssh_key(az_compute_auth: ComputeManagementClient):
    response = az_compute_auth.ssh_public_keys.generate_key_pair(
        resource_group_name = "Gaia",
        ssh_public_key_name = "gaia-redir"
    )

    # Dump the new keypair to disk at ~/.ssh/gaia.pem overwriting an existing pair. This should work across both windows and linux. 
    utils.redirector.generic.create_local_gaia_ssh_key(key_name="gaia-redir", key_contents=response.private_key)

    return response

def deploy_vm(az_compute_auth: ComputeManagementClient, region:str, vm_size:str, vm_os:str, net_interface_id:str, ssh_public_key:str, env:dict):
    # Get options for Ubuntu and Debian
    if vm_os == "ubuntu":
        image_publisher = "Canonical"
        image_offer = "ubuntu-24_04-lts"
        sku = "server"
        version = "latest"
    elif vm_os == "debian":
        image_publisher = "Debian"
        image_offer = "debian-13"
        sku = "13-gen2"
        version = "latest"
    else:
        print("Error in OS selection. This should never happen. Exiting!")
        sys.exit(1)

    username = utils.env.resolve_env_inputs(arg_parameter="gaia", env_key="REDIRECTOR_USER", env=env)

    result = az_compute_auth.virtual_machines.begin_create_or_update(
        resource_group_name = "Gaia",
        vm_name = "Gaia-Redir",
        parameters = VirtualMachine(
            location = region,
            tags = {
                "createdBy" : "Gaia"
            },
            hardware_profile = HardwareProfile(
                vm_size = vm_size
            ),
            storage_profile = StorageProfile(
                image_reference = ImageReference(
                    publisher = image_publisher,
                    offer = image_offer,
                    sku = sku,
                    version = version
                ),
                os_disk = OSDisk(
                    disk_size_gb = 30,
                    create_option = "FromImage",
                ),
            ),
            os_profile = OSProfile(
                computer_name = "Gaia-Redir",
                admin_username = username,
                linux_configuration = LinuxConfiguration(
                    disable_password_authentication = True,
                    ssh = SshConfiguration (
                        public_keys = [
                            SshPublicKey(
                                path = f"/home/{username}/.ssh/authorized_keys",
                                key_data = ssh_public_key,
                            ),
                        ]
                    ),
                ),
            ),
            network_profile = NetworkProfile(
                network_interfaces = [
                    NetworkInterfaceReference(
                        id = net_interface_id,
                        primary = True
                    )
                ]
            ),
        ),
    ).result()

    return result

def print_gaia_vms(az_network_auth: NetworkManagementClient, vm_list):
    table = PrettyTable(["VM ID", "VM Name", "Status", "Size", "Public IP"])

    for i in vm_list:
        # Get base VM Information
        vm_name = i["name"]
        vm_status = i.properties.provisioning_state
        vm_size = i.properties.hardware_profile.vm_size
        vm_id = i.properties.vm_id

        # Get the name of the NIC
        nic_id = i.properties.network_profile.network_interfaces[0].id
        nic_name_list = nic_id.split("/")
        nic_name = nic_name_list[-1]

        # Query NIC for reference to public IP address 
        nic_info = az_network_auth.network_interfaces.get(resource_group_name="Gaia", network_interface_name=nic_name)
        ip_name_list = nic_info.properties.ip_configurations[0].public_ip_address.id.split("/")
        ip_name = ip_name_list[-1]

        # Get the public IP address info
        ip_info = az_network_auth.public_ip_addresses.get(resource_group_name="Gaia", public_ip_address_name=ip_name)
        vm_ip_address = ip_info.properties.ip_address

        # Append to table
        table.add_row([vm_id, vm_name, vm_status, vm_size, vm_ip_address])

    print(table)