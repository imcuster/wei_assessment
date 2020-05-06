#!/usr/local/bin/python3

import argparse
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# Allow the user to optionally select a different AWS profile when running the script.
parser = argparse.ArgumentParser()
parser.add_argument('--env', help='Select the AWS profile you will run this script against.', default='default')
parser.add_argument('--unit', help='Select the unit for bucket size.', default='Bytes')
args = parser.parse_args()

# Define the AWS session and set up an empty list for later.
session = boto3.session.Session(profile_name=args.env)
region_name = 'us-east-1'
bucket_dict = {}

# Populate list of all accessible S3 buckets.
def list_buckets():
    s3 = session.client(service_name='s3', region_name=region_name)
    # Try to list S3 buckets, with example of exception caught.
    try:
        response = s3.list_buckets()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoCredentialsError':
            raise e
    else:
        for bucket in response['Buckets']:
            bucket_dict[bucket['Name']] = bucket['CreationDate']


def get_bucket_contents():
    s3 = session.client(service_name='s3',region_name='us-east-1')
    cw = session.client(service_name='cloudwatch',region_name='us-east-1')

    for bucket_key, bucket_val in bucket_dict.items():
        try:
            creation_date = bucket_val
            object_list = s3.list_objects(Bucket=bucket_key)
            file_descriptor = object_list['Contents']
            bucket_size = cw.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_key},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                Statistics=['Average'],
                Period=86400,
                StartTime=datetime.now() - timedelta(days=1),
                EndTime=datetime.now(),
                Unit=args.unit
                )
            #bucket_size_bytes = bucket_size['Datapoints'][-1]['Average']
            bucket_size_bytes = bucket_size['Datapoints']
            get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
            last_added = [obj['LastModified'] for obj in sorted(file_descriptor, key=get_last_modified, reverse=True)][0]


        except ClientError as e:
            # This would catch a misconfigured region_name, for example.
            if e.response['Error']['Code'] == 'EndpointConnectionError':
                raise e
        else:
            print("Bucket Name: ", bucket_key)
            print("Bucket Creation Date: ", creation_date)
            print("Number of Objects: ", len(file_descriptor))
            print("Bucket Size: ", bucket_size_bytes)
            print("Most Recent Item: ", last_added)


list_buckets()
get_bucket_contents()
