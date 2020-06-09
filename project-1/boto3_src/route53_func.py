#!/usr/bin/env python

import boto3, os

def add_host_record(client, lb_dns, lb_hosted_zone, fqdn, hosted_zone):
    add_record = client.change_resource_record_sets(
        ChangeBatch={
          'Changes': [
            {
              'Action': 'CREATE',
              'ResourceRecordSet': {
                'AliasTarget': {
                  'DNSName': lb_dns,
                  'EvaluateTargetHealth': False,
                  'HostedZoneId': lb_hosted_zone,
                },
                'Name': fqdn,
                'Type': 'A',
              },
            },
          ],
          'Comment': 'Alias to ELB for myawsblog.xyz',
        },
      HostedZoneId=hosted_zone,
    )
    return add_record
