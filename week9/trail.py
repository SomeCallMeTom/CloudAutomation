import boto3
import s3enforce
import json

sts_client = boto3.client("sts")
response = sts_client.get_caller_identity()
account_id = response["Account"]
# print(f"Account ID is {account_id}")


def CreateTrail(trail_name, bucket_name):
    trail = boto3.client("cloudtrail")
    try:
        create_response = trail.create_trail(
            Name=trail_name,
            S3BucketName=bucket_name
        )
        log_response = trail.start_logging(Name=trail_name)
        return (f"Trail {trail_name} successfully created")

    except trail.exceptions.TrailAlreadyExistsException as error:
        return (f"Trail {trail_name} Already Exists")
    except:
        return(f"An error occured!")


def StartLogging(trail_name):
    trail = boto3.client('cloudtrail')
    response = trail.start_logging(Name=trail_name)
    return response


def StopLogging(trail_name):
    trail = boto3.client('cloudtrail')
    response = trail.stop_logging(Name=trail_name)
    return response


def GetTrailStatus(trail_name):
    trail = boto3.client('cloudtrail')
    try:
        reponse = trail.get_trail_status(Name=trail_name)
        return response['IsLogging']
    except trail.exceptions.TrailNotFoundException as error:
        # print(f"Trail {trail_name} Does Not Exist!")
        raise NameError(f"Trail {trail_name} Was Not Found")
    except:
        print("Some other error ocurred")


if __name__ == "__main__":
    bucket_name = "tdarlington-trail-bucket"
    trail_name = "demo-cloud-trail"
    create_response = s3enforce.CreateBucket(bucket_name)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

    bucket_policy_response = s3enforce.SetBucketPolicy(
        bucket_name, json.dumps(policy))
    trail_response = CreateTrail(trail_name, bucket_name)

    trail_response = StopLogging(trail_name)
    if GetTrailStatus(trail_response):
        print(f"Trail {trail_name} is logging as expected")
    else:
        print(f"Trail {trail_name} is NOT logging, something is wrong")

    print(f"Trail Response: {trail_response}")
