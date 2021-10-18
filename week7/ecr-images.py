import boto3
import argparse

parser = argparse.ArgumentParser(
    description="This is to allow arguments for security group name")

parser.add_argument('-rn', '--repository-name', dest='repo_name',
                    default='', type=str, help='input the name of an ecr repository')

args = parser.parse_args()


ecr_client = boto3.client("ecr")


def Get_Repositories():
    repos = []
    response = ecr_client.describe_repositories()
    if not response['repositories']:
        print("Error! no repositories found")
        return None
    else:
        for repo in response['repositories']:
            repos.append(repo['repositoryName'])
        return repos


def Get_Images(repo_name=""):

    if len(repo_name) == 0:
        repos = Get_Repositories()
        if not repos:
            print("Error! Empty respositoryName")
        else:
            for repo in Get_Repositories():
                ecr_client.list_images(repositoryName=repo)
    else:
        ecr_client.list_images(repositoryName=repo_name)


if __name__ == "__main__":
    Get_Images(args.repo_name)
