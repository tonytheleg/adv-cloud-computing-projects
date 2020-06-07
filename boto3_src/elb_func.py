import boto3, os, sys, time

def create_lb(client, name, subnets: list, security_groups: list):
    elb = client.create_load_balancer(
        Name=name,
        Subnets=subnets,
        SecurityGroups=security_groups,
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': name
            },
        ],
        Type='application',
        IpAddressType='ipv4'
    )
    return elb

def create_target_group(client, name, vpc_id):
    target_group = client.create_target_group(
        Name=name,
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id
    )
    return target_group['TargetGroups'][0]['TargetGroupArn']

def register_targets(client, target_grp_arn, instance_id):
    client.register_targets(
        TargetGroupArn=target_grp_arn,
        Targets=[
            {
                'Id': instance_id
            },
        ]
    )

def create_http_listener(client, lb_arn, target_grp_arn):  
    client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP', 
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_grp_arn
            }
        ],
    )
def create_https_listener(client, lb_arn, cert_arn, target_grp_arn):
    client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTPS',
        Port=443,
        SslPolicy='ELBSecurityPolicy-2016-08',
        Certificates=[
            {
                'CertificateArn': cert_arn
            },
        ],
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_grp_arn,
            }
        ],
    )

def get_db_state(client, lb_arn):
    status = client.describe_load_balancers(LoadBalancerArns=[lb_arn])
    state = status['LoadBalancers'][0]['State']['Code']
    return state 