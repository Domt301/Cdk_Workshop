from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_ec2 as ec2,
    aws_lambda as _lambda
)


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # a vpc with 2 private subnets
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        # a security group with no ingress or egress rules
        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc)

        # four ec2 instances in the private subnets with amazon linux 2
        for i in range(4):
            ec2.Instance(self, "EC2Instance" + str(i), vpc=vpc, instance_type=ec2.InstanceType("t2.micro"), security_group=security_group, machine_image=ec2.MachineImage.latest_amazon_linux())
  

        # a Tag to identify the instances
        # ec2.Tag.add(self, "Name", "CDKWorkshop")

        # a lambda function to stop the instances
        # stop_instances = _lambda.Function(self, "StopInstances", runtime=_lambda.Runtime.PYTHON_3_7, handler="index.handler", code=_lambda.Code.asset("lambda"))
        # stop_instances.add_to_role_policy(iam.PolicyStatement(actions=["ec2:StopInstances"], resources=["*"]))
        # stop_instances.add_to_role_policy(iam.PolicyStatement(actions=["ec2:DescribeInstances"], resources=["*"]))


        # a lambda function to start the instances
        # start_instances = _lambda.Function(self, "StartInstances", runtime=_lambda.Runtime.PYTHON_3_7, handler="index.handler", code=_lambda.Code.asset("lambda"))
        # start_instances.add_to_role_policy(iam.PolicyStatement(actions=["ec2:StartInstances"], resources=["*"]))
        # start_instances.add_to_role_policy(iam.PolicyStatement(actions=["ec2:DescribeInstances"], resources=["*"]))

        # a step function to start the instances by invoking the lambda function
        # start_instances_step = _lambda.StepFunctionsStartExecutionStep("StartInstancesStep", parameters={"Input.$": "$"}, state_machine=start_instances)

        # a step function to stop the instances by invoking the lambda function
        # stop_instances_step = _lambda.StepFunctionsStartExecutionStep("StopInstancesStep", parameters={"Input.$": "$"}, state_machine=stop_instances)



        


