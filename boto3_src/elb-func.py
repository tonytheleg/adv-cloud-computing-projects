
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

def create_target_group(client, name, vpc_id):
    target_group = client.create_target_group(
        Name=name,
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id
    )
    return target_group['TargetGroups'][0]['TargetGroupArn']

def register_targets(client, target_grp_arn, instance_id):
    register = client.register_targets(
        TargetGroupArn=[target_grp_arn],
        Targets=[
            {
                'Id': instance_id
            },
        ]
    )

def create_http_listener(client, lb_arn, target_grp_arn    
    http_listener = client.create_listener(
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
