from aws_cdk import Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct


class VirtualPrivateCloud(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)

        self.max_zones: int = 2
        self.vpc_name: str = "sport_app_vpc"
        self.vpc = self.create_vpc()

    def create_vpc(self):
        vpc = ec2.Vpc(self, self.vpc_name, max_azs=self.max_zones, vpc_name=self.vpc_name)
        CfnOutput(self, "VpcId", value=vpc.vpc_id, export_name="VpcId")
        return vpc
