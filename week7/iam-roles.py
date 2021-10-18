import datetime
import pytz
import boto3


def Get_Recent_IAM_Policies():
    iam_client = boto3.client('iam')
    response = iam_client.list_policies()
    # print(response)
    for policy in response['Policies']:

        if policy['CreateDate'] > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
            print(policy['PolicyName'])
            print(policy['CreateDate'])


if __name__ == '__main__':
    Get_Recent_IAM_Policies()
