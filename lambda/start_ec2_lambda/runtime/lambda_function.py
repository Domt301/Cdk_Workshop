import os
import boto3
# get tag key and value from environment variables
tag_key = os.environ['TAG_KEY']
tag_value = os.environ['TAG_VALUE']
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # get all instances with the tag key and value
    response = ec2.describe_instances(Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])
    # get the instance ids
    instance_ids = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
    # start the instances
    ec2.start_instances(InstanceIds=instance_ids)
    print('started your instances: ' + str(instance_ids))