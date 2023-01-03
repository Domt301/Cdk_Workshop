import os
import boto3
# get tag key and value from environment variables
tag_key = os.environ['TAG_KEY']
tag_value = os.environ['TAG_VALUE']
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    print('got event: ' + str(event))
    # get all instances with the tag key and value
    response = ec2.describe_instances(Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])
    # get the instance ids
    instance_ids = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # ensure that instances are not already running or pending or shutting down or stopping or terminated
            if instance["State"]["Name"] not in ["running", "pending", "shutting-down", "stopping", "terminated"]:
                instance_ids.append(instance["InstanceId"])
    # start the instances
    # check if there are any instances to start
    if len(instance_ids) > 0:
        ec2.start_instances(InstanceIds=instance_ids)
    print('started your instances: ' + str(instance_ids))