import boto3
import json
from botocore.retries import bucket

s3 = boto3.client('s3')

bucket_name = 'week2-demo-tdarlington-ex2'

def to_json(self):
    return json.dumps(self, indent=4)
def pretty_print(o):
    print(to_json(o))

response = s3.create_bucket(Bucket=bucket_name)

#pretty_print(response)

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

policy_response = s3.put_bucket_policy(Bucket=bucket_name,Policy=bucket_policy)
#pretty_print(policy_response)

website_response  = s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
   }
)
#pretty_print(website_response)

index_file = open('index.html', 'rb')
index_reponse = s3.put_object(Body=index_file, Bucket=bucket_name, Key='index.html', ContentType='text/html')
index_file.close()
pretty_print(index_reponse)

error_file = open('error.html', 'rb')
error_response = s3.put_object(Body=error_file, Bucket=bucket_name, Key='error.html', ContentType='text/html')
error_file.close()
pretty_print(error_response)