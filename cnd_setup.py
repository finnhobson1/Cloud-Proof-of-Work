# Create AWS EC2 instances to run nonce discovery program.

import boto3
import time
import keyboard
import sys
import math


### CHANGE THIS PARAMETER TO YOUR PRIVATE BUCKET:
### -------------------------------
BUCKET_NAME = 'fh16413-cnd-output'
S3_ACCESS_ROLE = 'S3-Access'
LAMBDA_NAME = 'shutdownInstances'
### -------------------------------

ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')
lam = boto3.client('lambda')

bucket = s3.Bucket(BUCKET_NAME)
ami_id = 'ami-066be3e4e7954399c'
output_file = "output1"
data_block = "COMSM0010cloud"


def calculate_N(D, T, L):
    S = 35
    Y = 250000

    N = - (math.log(1-L)/(math.pow(0.5, D)*(T-S)*Y))
    
    N = int(math.ceil(N))

    return N


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
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            #KeyName='ec2-keypair',
            IamInstanceProfile={
                'Name': S3_ACCESS_ROLE
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
                    FunctionName=LAMBDA_NAME,
                    InvocationType='Event'
                )
                break
            else:
                print("Continuing search...")



if __name__ == '__main__':

    print()
    print("WECLOME TO FINN'S CLOUD NONCE DISCOVERY SYSTEM")
    print()
    
    difficulty_bits = int(input("Please enter the difficulty level (number of leading zeros) you would like: "))
    
    ### INPUT FOR INDIRECT SPECIFICATION OF N
    max_runtime = float(input("Please enter a desired maximum discovery time (minimum of 40 seconds): "))
    confidence = float(input("Please enter a desired confidence for this discovery time (decimal between 0 and 1): "))

    N_instances = calculate_N(difficulty_bits, max_runtime, confidence)

    ### INPUT FOR DIRECT SPECIFICATION OF N
    #N_instances = int(input("Please enter the number of workers (cloud instances) you would like to split the work between: "))

    print()
    print(f"Starting {N_instances} Cloud Instances...")

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

