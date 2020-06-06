#!/usr/bin/env python

import boto3, os

r53 = boto3.client('route53')

add_record = r53.change_resource_record_sets(
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'AliasTarget': {
                        'DNSName': os.environ.get('LB_DNS'),
                        'EvaluateTargetHealth': False,
                        'HostedZoneId': os.environ.get('LB_HOSTED_ZONE'),
                    },
                    'Name': 'myawsblog.xyz',
                    'Type': 'A',
                },
            },
        ],
        'Comment': 'Alias to ELB for myawsblog.xyz',
    },
    HostedZoneId='Z05892661O7M456HDD0PX',
)
