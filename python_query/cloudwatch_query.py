import boto3
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--profile', help='Select the AWS profile you will run this script with.', default='default')
args = parser.parse_args()


session = boto3.session.Session(profile_name=args.profile)
regions = session.get_available_regions('ec2')
def cloudwatch_query():
    cw = session.client(service_name='cloudwatch', region_name=region)
    disk_metrics = cw.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'disk_utilization',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'DiskWriteBytes',
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': 'i-0168822213433377a'
                            },
                        ]
                    },
                    'Period': 86400,
                    'Stat': 'DiskWriteBytes',
                    'Unit': 'Bytes'
                },
                'ReturnData': True
                #'Period': 86400,
                #'Stat': 'DiskWriteBytes'
            },
        ],
        StartTime=datetime.datetime(2020, 5, 1),
        EndTime=datetime.datetime(2020, 5, 6),
        ScanBy='TimestampDescending',
        MaxDatapoints=123
    )
    print(disk_metrics)

for region in regions:
    cloudwatch_query()
