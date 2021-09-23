from os import write
import re
import boto3, csv
import json
import datetime

def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def to_json(self):
    return json.loads(json.dumps(self, default=defaultconverter, indent=4))

def pretty_print(o):
    print(to_json(o))


def Get_Instances():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()
    # pretty_print(response['Reservations'][0]['Instances'])
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    #print(instances)
    return instances

def CSV_Writer(header,content):
    hFile = open('export.csv','w')
    writer = csv.DictWriter(hFile,fieldnames=header)
    writer.writeheader
    for line in content:
        writer.writerow(line)
    hFile.close()

def main():
    instances = Get_Instances()
    header = ['InstanceId','InstanceType','State','PublicIpAddress']
    content = []
    for instance in instances:
        print(f"Adding instance {instance['InstanceId']}")
        content.append(
            {
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "State": instance['State']['Name'],
                "PublicIpAddress": instance['PublicIpAddress']
            }
        )
    CSV_Writer(header,content)

if __name__ == "__main__":
    main()