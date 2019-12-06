import boto3
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    
    # Retrieve all EC2 instances with the "CNDAutoOff" tag
    filters = [{
            'Name': 'tag:CNDAutoOff',
            'Values': ['True']
        }
    ]
    
    # Filter the instances
    instances = ec2.instances.filter(Filters=filters)

    # Locate all running instances
    CNDInstances = [instance.id for instance in instances]
    
    # Make sure there are instances to shut down
    if len(CNDInstances) > 0:
        # Perform the shutdown
        shuttingDown = ec2.instances.filter(InstanceIds=CNDInstances).terminate()
        print(shuttingDown)
    else:
        print("No instances to shutdown")
    
    

