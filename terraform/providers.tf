terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"

  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "terraform-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    
    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  profile = "default"
  region  = var.region
}