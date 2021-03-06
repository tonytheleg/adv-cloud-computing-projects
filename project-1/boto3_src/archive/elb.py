#!/usr/bin/env python

import boto3, os, sys, time
elb = boto3.client('elbv2')
ec2_instance_id = os.environ.get('EC2_INSTANCE_ID')

wp_elb = elb.create_load_balancer(
    Name='wp-lb',
    Subnets=[
        'subnet-0de8e0b2402bda6c5',
        'subnet-01652e5314e269400',
    ],
    SecurityGroups=[
        'sg-0b5b3d85946596ab7',
    ],
    Scheme='internet-facing',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'wp-lb'
        },
    ],
    Type='application',
    IpAddressType='ipv4'
)

target_group = elb.create_target_group(
    Name='web-servers',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-0ed1045dd1bd534b1'
)


register = elb.register_targets(
    TargetGroupArn=target_group['TargetGroups'][0]['TargetGroupArn'],
    Targets=[
        {
            'Id': ec2_instance_id
        },
    ]
)

http_listener = elb.create_listener(
    LoadBalancerArn=wp_elb['LoadBalancers'][0]['LoadBalancerArn'],
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group['TargetGroups'][0]['TargetGroupArn']
        }
    ],
)

https_listener = elb.create_listener(
    LoadBalancerArn=wp_elb['LoadBalancers'][0]['LoadBalancerArn'],
    Protocol='HTTPS',
    Port=443,
    SslPolicy='ELBSecurityPolicy-2016-08',
    Certificates=[
        {
            'CertificateArn': 'arn:aws:acm:us-east-1:349440264862:certificate/3f08958f-7341-4883-84ce-0ca0df7f6202'
        },
    ],
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group['TargetGroups'][0]['TargetGroupArn'],
        }
    ],
)

LB_ARN = wp_elb['LoadBalancers'][0]['LoadBalancerArn']
check_state = ""

while check_state != "active":
    print("LB Creating...waiting for completion")
    status = elb.describe_load_balancers(LoadBalancerArns=[LB_ARN])
    check_state = status['LoadBalancers'][0]['State']['Code']
    if check_state == 'failed' or check_state == 'active_impaired':
        print("Uh oh, something went wrong with creating the elb")
        sys.exit(1)
    time.sleep(30)

print(f"Done.\nDNS: {wp_elb['LoadBalancers'][0]['DNSName']}\nHosted Zone: {wp_elb['LoadBalancers'][0]['CanonicalHostedZoneId']}")

