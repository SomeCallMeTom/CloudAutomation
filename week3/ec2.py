import boto3




#AMI = "ami-087c17d1fe0178315"
def Get_Image(ec2_client):

    images = ec2_client.describe_images(
        Filters=[
            {
                "Name": "name",
                "Values" : ["amzn2-ami-hvm*"]
            }
        ]
    )

    return images["Images"][0]["ImageId"]

def Create_EC2(AMI,ec2_client):

    response = ec2_client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    return response['Instances'][0]['InstanceId']

if __name__ == '__main__':
    DRYRUN = False

    ec2_client = boto3.client("ec2")
    ec2_instance = boto3.resource("ec2")
    AMI = Get_Image(ec2_client)
    instance_id = Create_EC2(AMI,ec2_client)
    ec2 = ec2_instance.Instance(instance_id)
    print(ec2.state['Name'])
    ec2.wait_until_running()
    print(ec2.state['Name'])
    ec2.terminate()
    ec2.wait_until_terminated()
    print(ec2.state['Name'])