# Set Terraform required version to keep things nice and current

terraform {
  required_version = ">= 0.12.24"
  backend "s3" {
    bucket  = "icuster-terraform-state"
    key     = "terraform-infra/sample.tfstate"
    encrypt = true
    region  = "us-east-1"
  }
}

variable "region" {
  default = "us-east-1"
}

provider "aws" {
  alias                   = "east"
  version                 = ">= 2.11"
  shared_credentials_file = "~/.aws/credentials"
  region                  = "us-east-1"
}

provider "aws" {
  alias                   = "west"
  version                 = ">= 2.11"
  shared_credentials_file = "~/.aws/credentials"
  region                  = "us-west-2"
}

module "ec2_east" {
  source = "../modules/ec2"
  region = "us-east-1"
  // #vpc_id     = data.aws_vpc.default.id
  // vpc       = data.aws_vpc.selected.id
  // vpc       = module.vpc.vpc_id
  providers = {
    aws = aws.east
  }
}

module "ec2_west" {
  source = "../modules/ec2"
  region = "us-west-2"
  // #vpc_id     = data.aws_vpc.default.id
  // vpc       = data.aws_vpc.selected.id
  providers = {
    aws = aws.west
  }
}
