#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error
import os

rds_db = "wordpressdb.cfbzbccmzaob.us-east-1.rds.amazonaws.com"
rds_db_pass = os.getenv("RDS_DB_PASS")

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection(rds_db, "wordpress", rds_db_pass)

cursor = connection.cursor()
query = f"GRANT ALL ON wordpress.* TO 'wordpress'@'{rds_db}' IDENTIFIED BY '{rds_db_pass}';"
cursor.execute(query)
cursor.execute("FLUSH PRIVILEGES;")

