import json
import boto3


def Stop_EC2():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:env',
                'Values': ['dev']
            }
        ]
    )
    InstanceIds = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            InstanceIds.append(instance['InstanceId'])
    stop_response = ec2_client.stop_instances(InstanceIds=InstanceIds)
    return stop_response


def lambda_handler(event, context):
    stop_response = Stop_EC2()
    Stopped_InstanceIds = []
    for instance in stop_response['StoppingInstances']:
        Stopped_InstanceIds.append(instance['InstanceId'])

    return {
        'statusCode': 200,
        'body': json.dumps(Stopped_InstanceIds)
    }
