from constructs import Construct
import aws_cdk as cdk
import os
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks
  
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
            ec2_1 = ec2.Instance(self, "EC2Instance" + str(i),vpc=vpc, instance_type=ec2.InstanceType("t2.micro"),security_group=security_group, machine_image=ec2.MachineImage.latest_amazon_linux())
            cdk.Tags.of(ec2_1).add("Group", "Lambda-Group")
  

        # a lambda function that starts the ec2 instances
        start_ec2_lambda = _lambda.Function(self,
         "StartEC2Lambda", 
         runtime=_lambda.Runtime.PYTHON_3_8, 
         handler="lambda_function.lambda_handler", 
         code=_lambda.Code.from_asset(
            os.path.join( "lambda", "start_ec2_lambda", "runtime")
            ), 
         timeout=Duration.seconds(30), environment={"TAG_KEY": "Group", "TAG_VALUE": "Lambda-Group"})
        # a lambda function that stops the ec2 instances
        stop_ec2_lambda = _lambda.Function(self, 
        "StopEC2Lambda", 
        runtime=_lambda.Runtime.PYTHON_3_8,
         handler="lambda_function.lambda_handler", 
         code=_lambda.Code.from_asset(
            os.path.join("lambda", "stop_ec2_lambda", "runtime")
         ), 
         timeout=Duration.seconds(30), environment={"TAG_KEY": "Group", "TAG_VALUE": "Lambda-Group"})

        # permissions for the lambda functions to start and stop ec2 instances
        start_ec2_lambda.add_to_role_policy(iam.PolicyStatement(actions=["ec2:StartInstances"], resources=["*"]))
        start_ec2_lambda.add_to_role_policy(iam.PolicyStatement(actions=["ec2:DescribeInstances"], resources=["*"]))
        stop_ec2_lambda.add_to_role_policy(iam.PolicyStatement(actions=["ec2:StopInstances"], resources=["*"]))
        stop_ec2_lambda.add_to_role_policy(iam.PolicyStatement(actions=["ec2:DescribeInstances"], resources=["*"]))

   


        start_ec2_step_function = sfn.StateMachine(self, "StartEC2StepFunction",
                                 definition=sfn_tasks.LambdaInvoke(self, "StartEC2Task",
                                     lambda_function=start_ec2_lambda))

        # a step function that stops the ec2 instances by invoking the stop lambda function
        stop_ec2_step_function = sfn.StateMachine(self, "StopEC2StepFunction",
                                 definition=sfn_tasks.LambdaInvoke(self, "StopEC2Task",
                                     lambda_function=stop_ec2_lambda))


        start_ec2_lambda.grant_invoke(start_ec2_step_function)
        stop_ec2_lambda.grant_invoke(stop_ec2_step_function)




        


