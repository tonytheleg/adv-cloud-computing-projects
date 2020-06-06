#!/usr/bin/env python

rds = boto3.client('rds')
rds_db_passwd = os.environ.get("RDS_DB_PASSWD")

def create_db_subnet(client, name, description, subnet_ids: list)
    print("Creating the db subnet group")
    db_subnet = client.create_db_subnet_group(
        DBSubnetGroupName=name,
        DBSubnetGroupDescription=description,
        SubnetIds=subnet_ids
    )

    if db_subnet['DBSubnetGroup']['SubnetGroupStatus'] != 'Complete':
        print("db subnet group failed to create -- aborting")
        sys.exit(1)

    print("db subnet group successfully created -- creating database")

def create_db(client, db_name, db_username, security_groups: list, db_subnetgroup)
    db_instance = client.create_db_instance(
        DBName=db_name,
        DBInstanceIdentifier=db_name,
        AllocatedStorage=20,
        DBInstanceClass='db.t2.micro',
        Engine='mysql',
        MasterUsername=db_username,
        MasterUserPassword=rds_db_passwd,
        VpcSecurityGroupIds=security_groups,
        DBSubnetGroupName=db_subnetgroup,
        PubliclyAccessible=False,
        MultiAZ=False,
        DeletionProtection=False,
    )
    
    db_status = ""
    while db_status != "failed":
        db_info = rds.describe_db_instances(DBInstanceIdentifier=db_name)
        db_status = db_info['DBInstances'][0]['DBInstanceStatus']
        if db_status == "available":
            print("Database created")
            break
        else:
            print("Creating database -- this can take a while...")
            time.sleep(60)
    
    db_host = db_info['DBInstances'][0]['Endpoint']['Address']
    return db_host
