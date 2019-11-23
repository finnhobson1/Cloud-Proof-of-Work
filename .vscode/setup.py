# Create AWS EC2 instance to run Proof-of-Work program.

import boto3

def start_instances(D, N):
    ec2 = boto3.resource('ec2')

    for i in range(N):

        output_file = "output" + str(i)

        init_script = """#!/bin/bash
    sudo yum install -y python36 
    aws s3 cp s3://fh16413-pow-bucket/pow_cloud.py /home/ec2-user/pow.py
    python36 /home/ec2-user/pow.py COMSM0010cloud """ + str(D) + """ """ + str(N) + """ """ + str(i) + """ > /home/ec2-user/""" + output_file + """
    aws s3 cp /home/ec2-user/""" + output_file + """ s3://fh16413-pow-bucket/""" + output_file + """ """

        # Create a new EC2 instance
        instances = ec2.create_instances(
            ImageId='ami-04de2b60dd25fbb2e',
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
                            'Key': 'powAutoOff',
                            'Value': 'True'
                        }
                    ]
                }
            ],
            UserData=init_script # file to run on instance init.
        )

if __name__ == '__main__':

    difficulty_bits = int(input("Please enter the number of difficulty bits you would like: "))
    N_instances = int(input("Please enter the number of EC2 instances you would like to split the work between: "))

    start_instances(difficulty_bits, N_instances)


'''
    INIT SCRIPT TO PRINT TO INDEX.HTML
    sudo yum update -y
    sudo yum install -y httpd24
    service httpd start
    chkconfig httpd on
    echo """ + str(i) + """ > /var/www/html/index.html
'''
