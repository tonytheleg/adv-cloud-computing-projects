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

def create_ec2_instance(client, key_name, subnet_id, security_groups: list):
    instance = client.create_instances(
        ImageId="ami-085925f297f89fce1", # ubuntu 18.04
        InstanceType="t2.micro",
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        NetworkInterfaces=[
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_id,
                'Groups': security_groups
            }
        ],
        UserData=user_data
    )

    instance_id = instance[0].id
    return instance_id
