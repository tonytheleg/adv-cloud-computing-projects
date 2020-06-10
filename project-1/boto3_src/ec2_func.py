import os, time, sys

def create_ec2_instance(client, key_name, subnet_id, security_groups: list, rds_db):
    rds_db_host = rds_db
    rds_db_passwd = os.environ.get('RDS_DB_PASSWD')
    user_data=f'''#!/bin/bash
    pushd /tmp
    git clone https://github.com/tonytheleg/adv-cloud-computing-projects.git
    bash ./adv-cloud-computing-projects/project-1/ec2-setup.sh {rds_db_host} {rds_db_passwd}
    '''
    
    instance = client.run_instances(
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
    
    instance_id = instance['Instances'][0]['InstanceId']

    # sometimes the check is a little too fast
    time.sleep(5)
    
    ec2_state = ""
    while ec2_state != "running":
        print("Checking for a running instance...")
        status = client.describe_instances(InstanceIds=[instance_id])
        ec2_state = status['Reservations'][0]['Instances'][0]['State']['Name']
        if ec2_state == "terminated" or ec2_state == "stopped":
            print("Uh oh, something went wrong")
            sys.exit(1)
        time.sleep(20)

    return instance_id
