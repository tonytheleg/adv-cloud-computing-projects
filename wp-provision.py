#!/usr/bin/python3

import boto3, os, sys
import boto3_src.rds_func as rds_fn
import boto3_src.ec2_func as ec2_fn

# check for needed vars
# Create DB group
# Create DB
# Create EC2 with user script to provision Wordpress and setup DB
# Create S3 bucket for wordpress
# Create ELB for web server using created cert
# Register ELB in DNS

# rds config
rds = boto3.client('rds')
rds_db_passwd = os.environ.get("RDS_DB_PASSWD")
rds_subnets = ['subnet-02dd2559044a87b64','subnet-059421f2d36cf4e0a']
rds_sg = ['sg-025ada11b570e67df']

# ec2 config
ec2_subnet = "subnet-0de8e0b2402bda6c5"
ec2_sg = ['sg-0b5b3d85946596ab7']
ec2 = boto3.resource('ec2')

# create rds subnet group - returns nothing
rds_db_subnet = rds_fn.create_db_subnet(rds, 'privatesub', 'subnet for db', rds_subnets) 

# create mysql rds - returns db name and sets as env var
rds_db = rds_fn.create_db(rds, 'wordpressdb', 'wordpress', rds_sg, 'privatesub')
os.environ['RDS_DB_HOST'] = rds_db

# create wordpress vm
ec2_instance = ec2_fn.create_ec2_instance(ec2, "ec2-ssh", ec2_subnet, ec2_sg) 

