# Create AWS EC2 instances to run nonce discovery program.

import boto3
import time
import keyboard
import sys


### CHANGE THESE PARAMETERS:
### -------------------------------
BUCKET_NAME = 'fh16413-cnd-output'
AMI_ID = 'ami-066be3e4e7954399c'
### -------------------------------

ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')
lam = boto3.client('lambda')

bucket = s3.Bucket(BUCKET_NAME)
output_file = "output1"
data_block = "COMSM0010cloud"


def clear_results():

    objs = list(bucket.objects.filter(Prefix=output_file))
    if len(objs) > 0:
        objs[0].delete()


def start_instances(D, N):

    for i in range(N):

        init_script = """#!/bin/bash
    cd /home/ec2-user/
    python36 pow.py """ + data_block + """ """ + str(D) + """ """ + str(N) + """ """ + str(i) + """ > """ + output_file + """
    aws s3 cp """ + output_file + """ s3://""" + BUCKET_NAME + """/""" + output_file + """ """

        # Create a new EC2 instance
        instances = ec2.create_instances(
            ImageId=AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='ec2-keypair',
            IamInstanceProfile={
                'Name': 'S3-Access'
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'CNDAutoOff',
                            'Value': 'True'
                        }
                    ]
                }
            ],
            UserData=init_script # commands to run on instance initialisation.
        )


def print_results():

    output_found = False

    while not output_found:
        
        objs = list(bucket.objects.filter(Prefix=output_file))
        if len(objs) > 0 and objs[0].key == output_file:
            print()
            print("***RESULT FOUND***")
            body = objs[0].get()['Body'].read().decode('utf-8') 
            print(body)
            output_found = True
        
        if keyboard.is_pressed('space'):
            print()
            print("Are you sure you want to initiate a scram? [y/N]")
            print("WARNING: This will end the current search.")

            scram = input()
            if 'y' in scram:
                print()
                print("Scram initiated. Shutting down instances...")
                lam.invoke(
                    FunctionName='shutdownInstances',
                    InvocationType='Event'
                )
                break
            else:
                print("Continuing search...")



if __name__ == '__main__':

    print()
    print("WECLOME TO FINN'S CLOUD NONCE DISCOVERY SYSTEM")
    print()
    
    difficulty_bits = int(input("Please enter the number of difficulty bits (leading zeros) you would like to achieve: "))
    N_instances = int(input("Please enter the number of workers (cloud instances) you would like to split the work between: "))

    print()
    print("Starting Cloud Instances...")

    start_time = time.time()

    clear_results()

    start_instances(difficulty_bits, N_instances)

    print()
    print("Finding Golden Nonce...")
    print()
    print("Press SPACE to scram (immediately terminate all instances)")

    print_results()

    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Total Discovery Time = {elapsed_time:.3f}s")
    print()






'''
    INIT SCRIPT TO PRINT TO INDEX.HTML
    sudo yum update -y
    sudo yum install -y httpd24
    service httpd start
    chkconfig httpd on
    echo """ + str(i) + """ > /var/www/html/index.html
'''
