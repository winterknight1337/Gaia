import boto3, os

def create_aws_key_pair(ec2_session: boto3.Session.client, key_name: str, dry_run:bool=False):
    # Create the keypair "gaia" in AWS
    response = ec2_session.create_key_pair(
        KeyName=key_name,
        TagSpecifications=[
            {
                "ResourceType": "key-pair",
                "Tags": [
                    {
                        "Key": "createdBy",
                        "Value": "gaia"
                    },
                ]
            },
        ],
        DryRun=dry_run,
    )
    response_key_name = response["KeyName"]

    # Dump the new keypair to disk at ~/.ssh/gaia.pem overwriting an existing pair. This should work across both windows and linux. 
    home_dir = os.path.expanduser("~")
    ssh_dir = f"{home_dir}/.ssh/"
    with open(f"{ssh_dir}/{response_key_name}.pem", "w") as file:
        file.write(response["KeyMaterial"])

    return response_key_name

def create_aws_security_group(ec2_session: boto3.Session.client, dry_run:bool=False):
    response = ec2_session.create_security_group(
        Description="Created by Gaia",
        GroupName="Webservers",
        TagSpecifications=[
            {
                "ResourceType": "security-group",
                "Tags": [
                    {
                        "Key": "createdBy",
                        "Value": "gaia"
                    },
                ]
            },
        ],
        DryRun=dry_run
    )

    security_group_id = response["GroupId"]

    return security_group_id


def create_aws_security_group_entry(ec2_session: boto3.Session.client, security_group_id:str, transport_protocol:str, port: int, dry_run:bool=False):
    response = ec2_session.authorize_security_group_ingress(
        CidrIp = "0.0.0.0/0",
        GroupId = security_group_id,
        IpProtocol = transport_protocol,
        FromPort = port,
        ToPort = port,
        TagSpecifications=[
            {
                "ResourceType": "security-group-rule",
                "Tags": [
                    {
                        "Key": "createdBy",
                        "Value": "gaia"
                    },
                ]
            },
        ],
        DryRun=dry_run
    )

    return response

def launch_ec2(ec2_session: boto3.Session.client, os: str, ec2_size: str, key_name: str, security_group_id: str, dry_run:bool=False):

    if os == "ubuntu":
        ImageId="ami-0e5497a77ef21b5ac"
    elif os == "debian":
        ImageId="ami-0e68dc81dc36750a1"

    response = ec2_session.run_instances(
        BlockDeviceMappings=[
            {
                "Ebs": {
                    "DeleteOnTermination": True,
                    "Iops" : 3000,
                    "VolumeSize": 30,
                    "VolumeType": "gp3",
                    "Throughput" : 125,
                },
                "DeviceName" : "/dev/sda1"
            },
        ],
        ImageId=ImageId,
        InstanceType=ec2_size,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "createdBy",
                        "Value": "gaia"
                    },
                ]
            },
        ],
        DryRun=dry_run
    )

    return response

def get_aws_network_interface_public_ip(ec2_session: boto3.Session.client, interface_id: str, dry_run:bool=False):
    response = ec2_session.describe_network_interfaces(
        NetworkInterfaceIds = [
            interface_id,
        ],
        DryRun = dry_run
    )

    return response

def get_gaia_ec2s(ec2_session: boto3.Session.client, dry_run:bool=False):
    response = ec2_session.describe_instances(
        Filters = [
            {
                "Name" : "tag:createdBy",
                "Values": [
                    "gaia",
                ]
            },
        ],
        DryRun = dry_run
    )
    MaxResults = 1000

    return response

def get_gaia_key_pairs(ec2_session: boto3.Session.client, dry_run:bool=False):
    response = ec2_session.describe_key_pairs(
       Filters = [
            {
                "Name" : "tag:createdBy",
                "Values": [
                    "gaia",
                ]
            },
        ],
        DryRun = dry_run
    )

    return response

def get_gaia_security_groups(ec2_session: boto3.Session.client, dry_run:bool=False):
    response = ec2_session.describe_security_groups(
        Filters = [
            {
                "Name" : "tag:createdBy",
                "Values": [
                    "gaia",
                ]
            },
        ],
        DryRun = dry_run
    )

    return response

def terminate_gaia_instances(ec2_session: boto3.Session.client, instance_ids:list, dry_run:bool=False):
    response = ec2_session.terminate_instances(
        InstanceIds=instance_ids,
        DryRun = dry_run)

    return response

def delete_gaia_ssh_keys(ec2_session: boto3.Session.client, key_pair_id:str, dry_run:bool=False):
    response = ec2_session.delete_key_pair(
        KeyPairId = key_pair_id,
        DryRun = dry_run
    )

    return response

def delete_gaia_security_groups(ec2_session: boto3.Session.client, group_id:str, dry_run:bool=False):
    response = ec2_session.delete_security_group(
        GroupId = group_id,
        DryRun = dry_run
    )

    return response