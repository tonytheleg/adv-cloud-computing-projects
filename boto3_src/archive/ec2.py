#!/usr/bin/env python

import boto3
import os, sys, time

rds_db_host = os.environ.get('RDS_DB_HOST')
rds_db_passwd = os.environ.get('RDS_DB_PASSWD')

#user_data=f'''#!/bin/bash
#pushd /tmp
#git clone https://github.com/tonytheleg/adv-cloud-computing-projects.git
#bash ./adv-cloud-computing-projects/ec2-setup.sh {rds_db_host} {rds_db_passwd}
#'''

ec2 = boto3.client('ec2')

instance = ec2.run_instances(
    ImageId="ami-085925f297f89fce1", # ubuntu 18.04
    InstanceType="t2.micro",
    MinCount=1,
    MaxCount=1,
    KeyName="ec2-ssh",
    NetworkInterfaces=[
        {
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'SubnetId': "subnet-0de8e0b2402bda6c5",
            'Groups': [
                'sg-0b5b3d85946596ab7'
            ]
        }
    ],
#    UserData=user_data
)

instance_id = instance['Instances'][0]['InstanceId']
print(f"Instance ID: {instance_id}")

# sometimes the check is a little too fast
time.sleep(5)

ec2_state = ""
while ec2_state != "running":
    print("Checking for a running instance...")
    status = ec2.describe_instances(InstanceIds=[instance_id])
    ec2_state = status['Reservations'][0]['Instances'][0]['State']['Name']
    if ec2_state == "terminated" or ec2_state == "stopped":
        print("Uh oh, something went wrong")
        sys.exit(1)
    time.sleep(20)

