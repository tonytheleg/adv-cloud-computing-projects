#!/usr/bin/env python

import boto3
import os

rds_db_host = os.environ.get('RDS_DB_HOST')
rds_db_passwd = os.environ.get('RDS_DB_PASSWD')
user_data=f'''#!/bin/bash
pushd /tmp
git clone https://github.com/tonytheleg/adv-cloud-computing-projects.git
bash ./adv-cloud-computing-projects/ec2-setup.sh {rds_db_host} {rds_db_passwd}
'''

ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
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
    UserData=user_data
)
