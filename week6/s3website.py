import boto3
import json
import argparse
import string
import random
import botocore

from botocore.retries import bucket

s3 = boto3.client('s3')

bucket_name = 'week6-demo-tdarlington-'

parser = argparse.ArgumentParser(
    description="This is to allow arguments for my s3website script")

parser.add_argument('-s', '--site-name', dest='site_name',
                    default='', type=str, help='Enter a unique bucket name')

args = parser.parse_args()
print(args.site_name)
if not args.site_name:
    print(f"No site-name provided, generating random")
    bucket_name += "".join(random.choices(string.ascii_lowercase, k=10))
else:
    bucket_name = args.site_name


def to_json(self):
    return json.dumps(self, indent=4)


def pretty_print(o):
    print(to_json(o))


try:
    response = s3.create_bucket(Bucket=bucket_name)

    # pretty_print(response)

    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket_name
        }]
    }
    bucket_policy = to_json(bucket_policy)
    #print( bucket_policy)

    policy_response = s3.put_bucket_policy(
        Bucket=bucket_name, Policy=bucket_policy)
    # pretty_print(policy_response)

    website_response = s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
    )
    # pretty_print(website_response)

    index_file = open('index.html', 'rb')
    index_reponse = s3.put_object(
        Body=index_file, Bucket=bucket_name, Key='index.html', ContentType='text/html')
    index_file.close()
    pretty_print(index_reponse)

    error_file = open('error.html', 'rb')
    error_response = s3.put_object(
        Body=error_file, Bucket=bucket_name, Key='error.html', ContentType='text/html')
    error_file.close()
    pretty_print(error_response)

except botocore.exceptions.ClientError as error:
    # print(error)
    if error.response['Error']['Code'] == 'InvalidToken':
        print("Please update your aws credentials with a valid token")
    else:
        print(f"some other error occured {error}")
