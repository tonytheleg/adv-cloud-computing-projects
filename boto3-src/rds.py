#!/usr/bin/env python

import boto3
import time
import os

rds_db_pass = os.getenv("RDS_DB_PASS"),
rds = boto3.client('rds')

print("Creating the db subnet group")
db_subnet = rds.create_db_subnet_group(
    DBSubnetGroupName='privatesub',
    DBSubnetGroupDescription='private subnet for RDS',
    SubnetIds=[
        'subnet-02dd2559044a87b64',
        'subnet-059421f2d36cf4e0a',
    ]
)

if db_subnet['DBSubnetGroup']['SubnetGroupStatus'] != 'Complete':
    print("db subnet group failed to create -- aborting")
    os.exit(1)

print("db subnet group successfully created -- creating database")
db_instance = rds.create_db_instance(
    DBName='wordpressdb',
    DBInstanceIdentifier='wordpressdb',
    AllocatedStorage=20,
    DBInstanceClass='db.t2.micro',
    Engine='mysql',
    MasterUsername='wordpress',
    MasterUserPassword=rds_db_pass,
    VpcSecurityGroupIds=[
        'sg-025ada11b570e67df',
    ],
    DBSubnetGroupName='privatesub',
    PubliclyAccessible=True,
    MultiAZ=False,
    DeletionProtection=False,
)

db_status = ""
while db_status != "failed":
    db_info = rds.describe_db_instances(DBInstanceIdentifier='wordpressdb')
    db_status = db_info['DBInstances'][0]['DBInstanceStatus']
    if db_status == "available":
        print("Database created")
        break
    else:
        print("Creating database -- this can take a while...")
        time.sleep(60)

print(f"Database Endpoint: {db_info['DBInstances'][0]['Endpoint']['Address']}")

