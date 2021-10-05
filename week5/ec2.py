import boto3
DRYRUN = False
#AMI = "ami-087c17d1fe0178315"


def Get_Image(ec2_client):

    images = ec2_client.describe_images(
        Filters=[
            {
                "Name": "name",
                "Values": ["amzn2-ami-hvm*"]
            }
        ]
    )

    return images["Images"][0]["ImageId"]


def Create_EC2(AMI, ec2_client):

    response = ec2_client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN,
        SecurityGroups=['WebSG'],
        UserData='''
            #!/bin/bash -ex
            # Updated to use Amazon Linux 2
            yum -y update
            yum -y install httpd php mysql php-mysql
            /usr/bin/systemctl enable httpd
            /usr/bin/systemctl start httpd
            cd /var/www/html
            wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/lab6-scaling/lab-app.zip
            unzip lab-app.zip -d /var/www/html/
            chown apache:root /var/www/html/rds.conf.php
        '''
    )
    return response['Instances'][0]['InstanceId']


def Print_Tags(ec2):
    tags = ec2.tags
    if tags is not None:
        for tag in tags:
            print(tag['Key']+" = "+tag['Value'])
    else:
        print("no tags found")


def Create_Tag(ec2, key, value):
    ec2.create_tags(
        DryRun=DRYRUN,
        Tags=[
            {
                'Key': key,
                'Value': value
            },
        ]
    )


if __name__ == '__main__':

    ec2_client = boto3.client("ec2")
    ec2_instance = boto3.resource("ec2")
    AMI = Get_Image(ec2_client)
    instance_id = Create_EC2(AMI, ec2_client)
    ec2 = ec2_instance.Instance(instance_id)
    print(ec2.state['Name'])
    ec2.wait_until_running()
    ec2 = ec2_instance.Instance(instance_id)
    print(ec2.state['Name'])
    print(ec2.public_ip_address)
    Print_Tags(ec2)
    Create_Tag(ec2, "Name", "Thomas")
    Print_Tags(ec2)
    ec2.terminate()
    ec2.wait_until_terminated()
    print(ec2.state['Name'])
