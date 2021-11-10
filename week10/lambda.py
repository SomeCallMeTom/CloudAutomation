import boto3


def CreateLambda(functionName):

    iam_client = boto3.client('iam')
    role_response = iam_client.get_role(RoleName='LabRole')

    handler = open('lambda_start_function.zip', 'rb')
    zipped_code = handler.read()

    lambda_client = boto3.client('lambda')
    response = lambda_client.create_function(
        FunctionName=functionName,
        Role=role_response['Role']['Arn'],
        Publish=True,
        PackageType='Zip',
        Runtime='python3.9',
        Code={'ZipFile': zipped_code},
        Handler='lambda_start_function.lambda_handler'
    )
    return response


def InvokeLambda(functionName):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName=functionName)
    return response


def main():
    functionName = "StartEC2"
    lambda_client = boto3.client('lambda')
    try:
        function = lambda_client.get_function(FunctionName=functionName)
        print(f"Existing {functionName} Function Found")
    except lambda_client.exceptions.ResourceNotFoundException:
        print("Creating Function...")
        response = CreateLambda(functionName)
        print(f"Created Function: {functionName}")

    response = InvokeLambda(functionName)
    print(f"Status Code: {response['StatusCode']}")


if __name__ == "__main__":
    main()
