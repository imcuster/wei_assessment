# wei_assessment
This repository has two segments: a Terraform deployment into AWS, and a boto3 query to get information about that deployment.

# Terraform
## Installation
Installing Terraform can be quite simple depending on your OS.  On OS X, you can simply run `brew install terraform`.  Steps for other operating systems are covered here: https://learn.hashicorp.com/terraform/getting-started/install.html
Verify your installation worked by opening a new terminal session and running `terraform -help`.
## Getting the code running
You'll note that the backend for this deployment is a bucket on my personal S3 account.  You'll need to change that to a bucket you own if you want to run this in your own environment.
Once you have your environment set up, `cd` to `terraform-infra/sample_deployment` and run the following commands:
- `terraform init` to initialize the AWS provider, modules, and backend.
- `terraform validate` to test for validity of the HCL code.
- (Optional) `terraform fmt` to automatically clean up indentation and style in your Terraform files.
- `terraform plan` to see what will be built or changed.
- `terraform apply` to create the defined resources.
Terraform is idempotent, meaning that you can run the `apply` command multiple times without constantly changing your state.  Terraform will refer to its state file to see what resources already exist, and the apply command will check to see what will change, what will be deleted, and what will be created.  If you haven't made any changes in your code, nothing will happen.

# Python / boto3 query
## Installation
From the `python_query` folder, run `pip install -r requirements.txt` to install `boto3` and `openpyxl` on your system.  These libraries interact with AWS and Microsoft Excel, respectively.

## Running the query
To get a list of options you can pass in to the query, run `python3 ec2_query --help`.  You can set your AWS profile (listed in `~/.aws/config`) and specify a region to run the script against.  By default, it will use the default profile and run against all available regions.
