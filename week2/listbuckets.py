import boto3
import json
import datetime

def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def to_json(self):
    return json.loads(json.dumps(self, default=defaultconverter, indent=4))

def pretty_print(o):
    print(to_json(o))

client = boto3.client('s3')

response = client.list_buckets()
# print("response")
# pretty_print(response)

format_response = to_json(response)
for bucket in response['Buckets']:
    print('Bucket: '+bucket['Name'])
    objects = client.list_objects_v2(Bucket=bucket['Name'])
    objects = to_json(objects)
    # print("objects")
    # print(objects)
    if "Contents" in objects:
        # print (len(objects["Contents"]))
        for content in objects['Contents']:
            print("    "+content['Key'])
    else:
        print("    ! Bucket does not have content !")
    