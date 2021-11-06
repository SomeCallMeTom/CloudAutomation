import json
import boto3


def Start_EC2():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances()
    InstanceIds = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            InstanceIds.append(instance['InstanceId'])
    start_response = ec2_client.start_instances(InstanceIds=InstanceIds)
    return start_response


def lambda_handler(event, context):
    start_response = Start_EC2()
    Started_InstanceIds = []
    for instance in start_response['StartingInstances']:
        Started_InstanceIds.append(instance['InstanceId'])
    return {
        'statusCode': 200,
        'body': json.dumps(Started_InstanceIds)
    }
