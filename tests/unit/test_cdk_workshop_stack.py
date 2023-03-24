import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


# test to confirm that the vpc is created
def test_vpc_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::EC2::VPC", 1)

# test to confirm that the security group is created
def test_security_group_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::EC2::SecurityGroup", 1)


# test to confirm that the lambda function is created
def test_lambda_function_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 2)

# test to confirm that step functions are created
def test_step_functions_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::StepFunctions::StateMachine", 2)

# test to confirm that the ec2 instances are created
def test_ec2_instances_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::EC2::Instance", 5)




