import random
import boto3
import argparse
import json

parser = argparse.ArgumentParser(
    description="This is to allow arguments for security group name")

parser.add_argument('-sg', '--security-group-name', dest='sg_name',
                    default='', type=str, help='input the name of an ec2 security group')

args = parser.parse_args()


def to_json(self):
    return json.dumps(self, indent=4)


def pretty_print(o):
    print(to_json(o))


def Get_Security_Groups(group_name):
    ec2_client = boto3.client("ec2")
    response = ""
    if not group_name:
        response = ec2_client.describe_security_groups()
    else:
        response = ec2_client.describe_security_groups(GroupNames=[group_name])
    for group in response["SecurityGroups"]:
        # for ipPermission in group["IpPermissionsEgress"]:
        for ipPermission in group["IpPermissions"]:
            if not ipPermission["IpRanges"]:
                continue
            else:
                for range in ipPermission["IpRanges"]:
                    if range["CidrIp"] in ["0.0.0.0/0", "0.0.0.0"]:
                        print(
                            f"Warning! GroupName {group['GroupName']} has a Cidr of {range['CidrIp']} this is open to the public internet!")

    pretty_print(response)


if __name__ == '__main__':
    Get_Security_Groups(args.sg_name)
