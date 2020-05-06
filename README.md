# wei_assessment
This repository has two segments: a Terraform deployment into AWS, and a boto3 query to get information about that deployment.
## Objective
Create a CLI script that audits all the VMs in a single AWS Region or multiple AWS Regions for the following information

   - The name of the VM
   - The instance ID of the VM
   - The region of the VM
   - The VPC of the VM
   - The number of attached disks (support for multiple disks is a requirement)
   - The mount points of all attached disks
   - The total size of each attached disk
   - The total space consumed within each attached disk

...then dump each field for each VM to an Excel spreadsheet with one region per tab of the spreadsheet.

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

# Progress notes
- I got a little too fancy with my Terraform and had to chase down an error in my configuration.  Turns out the `size` parameter for an aws_ebs_volume resource in Terraform is a little picky.  You might see a lot of lines that are commented out in the code; they represent features that I haven't restored yet.  They're not essential for running the code, just nice things to have.
- I wrote a boto3 script to pull information from my EC2 instances.  The basic requirements (name, instance ID, volume IDs + mount points, and etc) were easy enough, but to find the utilized disk space I need to turn to the CloudWatch portion of boto3.  As I understand it, boto3 works on the hypervisor layer, so using the EC2 portion of it can get surface information, but things that are accessible within the OS (aka the contents of your /proc folder) require a bit of maneuvering.  You can actually see an example of using CloudWatch to get information about S3 usage in the previous repo I sent you.
- I intended on using the `openpxyl` library to interact with Excel spreadsheets.  Unfortunately, installing it (or attempting to install it) led to another rabbit hole - the most recent OS X upgrade looks like it caused some issues with my Python / pip settings.  In the interest of time, instead of troubleshooting my OS X issue, I'll probably just try to complete the code on an Ubuntu VM.  
- I determined two solutions to the `openpyxl` installation.  My first instinct was to set up a simple EC2 instance and run my code from there; however, a quicker solution was to simply use a python virtual environment: `python3 -m venv env` followed by `source env/bin/activate`.  This allowed me to install my packages and move on unimpeded.
- Official AWS documentation led me to https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html as a method for programmatically obtaining disk usage metrics via CloudWatch.  This involves creating an IAM role for your instances and running Perl scripts to inject custom metrics into CloudWatch.  
