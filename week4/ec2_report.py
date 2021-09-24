from os import write
from warnings import filters
import boto3
import csv


def Get_Instances(filter_name, value):
    ec2_client = boto3.client('ec2')
    #response = ec2_client.describe_instances()
    paginator = ec2_client.get_paginator('describe_instances')
    pages = paginator.paginate(
        Filters=[
            {
                'Name': filter_name,
                'Values': [value]
            },
        ]
    )
    # pretty_print(response['Reservations'][0]['Instances'])
    instances = []
    for page in pages:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)
                # print(instance)
    return instances


def CSV_Writer(header, content):
    hFile = open('export.csv', 'w')
    writer = csv.DictWriter(hFile, fieldnames=header)
    writer.writeheader
    for line in content:
        writer.writerow(line)
    hFile.close()


def main():
    instances = Get_Instances('instance-state-name', 'running')
    header = ['InstanceId', 'InstanceType', 'State', 'PublicIpAddress']
    content = []
    for instance in instances:
        print(f"Adding instance {instance['InstanceId']}")
        content.append(
            {
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "State": instance['State']['Name'],
                "PublicIpAddress": instance.get('PublicIpAddress', "N/A")
            }
        )
    CSV_Writer(header, content)


if __name__ == "__main__":
    main()
