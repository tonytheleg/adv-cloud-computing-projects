#!/usr/bin/env python

import boto3

s3 = boto3.client('s3')

bucket = s3.create_bucket(
        ACL='public-read',
        Bucket='anatale-wpbucket-myawsblog'
)

print(bucket)
