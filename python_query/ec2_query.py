#!/usr/local/bin/python3

import boto3
import argparse
from openpyxl import Workbook

parser = argparse.ArgumentParser()
parser.add_argument('--profile', help='Select the AWS profile you will run this script with.', default='default')
parser.add_argument('--region', help='Select the region you will run this script against.', default='us-east-1')
args = parser.parse_args()

session = boto3.session.Session(profile_name=args.profile)
regions = session.get_available_regions('ec2')

def list_instances():
    ec2 = session.client(service_name='ec2', region_name=region)
    instances = ec2.describe_instances()
    disk_info = ec2.describe_volumes()
    volume_size = disk_info['Volumes']
    for instance in instances['Reservations']:
        instance_dict = instance['Instances']
        for item in instance_dict:
            # This script can fail if it runs into a terminated instance.
            if item['State']['Name'] == 'terminated':
                break
            # Get a list of attached volumes to user later
            volume_info = item['BlockDeviceMappings']
            # Get the instance ID
            print("Instance ID:", item['InstanceId'])
            # Get the VPC it lives in
            # It appears this fails if there's a terminated instance in your list?
            print("VPC:", item['VpcId'])
            # Get the number of attached disks
            print("Number of attached disks:", len(volume_info))
            # Get information about attached volumes
            for volume in volume_info:
                volume_id = volume['Ebs']['VolumeId']
                print("Volume ID:", volume_id)
                print("Volume mount point:", volume['DeviceName'])
                print("Volume size:", volume_size)

for region in regions:
    print("Region:", region)
    list_instances()
