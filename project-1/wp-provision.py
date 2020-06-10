#!/usr/bin/python3

from boto3_src.route53_func import add_host_record
import boto3, os, sys, time

# local imports
import boto3_src.rds_func as rds_fn
import boto3_src.ec2_func as ec2_fn
import boto3_src.elb_func as elb_fn
import boto3_src.route53_func as r53_fn

# global config
vpc_id = "vpc-0ed1045dd1bd534b1"
cert_arn = "arn:aws:acm:us-east-1:349440264862:certificate/3f08958f-7341-4883-84ce-0ca0df7f6202"
hosted_zone = "Z05892661O7M456HDD0PX"

# rds config
rds = boto3.client('rds')
rds_db_passwd = os.environ.get("RDS_DB_PASSWD")
rds_subnets = ['subnet-02dd2559044a87b64','subnet-059421f2d36cf4e0a']
rds_sg = ['sg-025ada11b570e67df']

# ec2 config
ec2_subnet = "subnet-0de8e0b2402bda6c5"
ec2_sg = ['sg-0b5b3d85946596ab7']
ec2 = boto3.client('ec2')

# elb config
elb = boto3.client('elbv2')
elb_subnets = ['subnet-0de8e0b2402bda6c5', 'subnet-01652e5314e269400']
elb_sg = ['sg-0b5b3d85946596ab7']

# route53 config
r53 = boto3.client('route53')

# create rds subnet group - returns nothing
rds_db_subnet = rds_fn.create_db_subnet(rds, 'privatesub', 'subnet for db', rds_subnets) 

# create mysql rds - returns db name and sets as env var
rds_db = rds_fn.create_db(rds, 'wordpressdb', 'wordpress', rds_sg, 'privatesub')

# create wordpress vm
ec2_instance = ec2_fn.create_ec2_instance(ec2, "ec2-ssh", ec2_subnet, ec2_sg, rds_db) 
print(f"Instance Created: {ec2_instance}")

# create lb
wp_elb = elb_fn.create_lb(elb, 'wp-lb', elb_subnets, elb_sg)

# get lb state
check_state = ""
while check_state != "active":
    print("LB Creating...waiting for completion")
    check_state = elb_fn.get_db_state(elb, lb_arn)
    if check_state == 'failed' or check_state == 'active_impaired':
        print("Uh oh, something went wrong with creating the elb")
        sys.exit(1)
    time.sleep(30)

# get elb config now that its done
lb_arn = wp_elb['LoadBalancers'][0]['LoadBalancerArn']
lb_dns = wp_elb['LoadBalancers'][0]['DNSName']
lb_hosted_zone = wp_elb['LoadBalancers'][0]['CanonicalHostedZoneId']

# create and register the target group
target_group = elb_fn.create_target_group(elb, 'webservers', vpc_id)
elb_fn.register_targets(elb, target_group, ec2_instance)

# create the listeners
elb_fn.create_http_listener(elb, lb_arn, target_group)
elb_fn.create_https_listener(elb, lb_arn, cert_arn, target_group)

print("ELB Created") 

# register the elb in dns
add_record = r53_fn.add_host_record(r53, lb_dns, lb_hosted_zone, 'myawsblog.xyz', hosted_zone)
print("DNS records added...")
print("PROVISIONING COMPLETE!")
