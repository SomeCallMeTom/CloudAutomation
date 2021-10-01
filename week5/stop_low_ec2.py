import ec2
import boto3

DRYRUN = False

sts_client = boto3.client("sts")
response = sts_client.get_caller_identity()
account_id = response["Account"]
print(f"Account ID is {account_id}")

ec2_client = boto3.client('ec2')

image_id = ec2.Get_Image(ec2_client)

cw_client = boto3.client.("cloudwatch")
