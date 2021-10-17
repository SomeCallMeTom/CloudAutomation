import datetime
import pytz
import boto3


def Print_Recent_IAM_Policies():
    recent_polices = []
    response = iam_client.list_policies()
    # print(response)
    for policy in response['Policies']:

        if policy['CreateDate'] > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
            print(policy['PolicyName'])
            print(policy['CreateDate'])


if __name__ == '__main__':
    iam_client = boto3.client('iam')
    policies = Print_Recent_IAM_Policies()
