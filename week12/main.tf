terraform {
  backend "remote" {
    organization = "fall-21-adv-scrpt"

    workspaces {
      name = "demo"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}
data "aws_iam_role" "lab_role" {
  name = "LabRole"
}
resource "aws_lambda_function" "Upload-stopEC2" {
  filename      = "stopEC2.zip"
  function_name = "tom-stopEC2"
  role          = data.aws_iam_role.lab_role.arn
  runtime       = "python3.9"
  handler       = "stopEC2.lambda_handler"
}
resource "aws_lambda_function" "Upload-startEC2" {
  filename      = "startEC2.zip"
  function_name = "tom-startEC2"
  role          = data.aws_iam_role.lab_role.arn
  runtime       = "python3.9"
  handler       = "startEC2.lambda_handler"
}
